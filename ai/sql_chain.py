"""
Configuração do LangChain SQL Chain +pgvector para consultas híbridas (Text-to-SQL + Busca Semântica).
Otimizado para performance usando LCEL (LangChain Expression Language).
"""

from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import text
from sqlalchemy.orm import Session
import os
import logging
import re

logger = logging.getLogger(__name__)


class SQLChain:
    """
    Chain híbrida para geração de SQL e busca semântica com pgvector
    a partir de perguntas em linguagem natural.
    """

    def __init__(self, ai_provider: str = "groq"):
        """
        Inicializa a chain híbrida.

        Args:
            ai_provider: Provider de IA ('openai' ou 'groq')
        """
        self.ai_provider = ai_provider
        self.llm = self._create_llm()
        self.sql_chain = self._create_sql_chain()
        self.response_chain = self._create_response_chain()

    def _create_llm(self):
        """Cria a instância do LLM baseado no provider configurado."""
        if self.ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY não configurada")
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                openai_api_key=api_key,
                max_tokens=500,
                timeout=30.0,
            )
        elif self.ai_provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY não configurada")
            return ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0,
                groq_api_key=api_key,
                max_tokens=500,
                timeout=30.0,
            )
        else:
            raise ValueError(f"Provider não suportado: {self.ai_provider}")

    def _create_sql_chain(self):
        """Cria a chain SQL usando LCEL."""
        system_prompt = """Você é um especialista em SQL e Engenharia de Dados. Converta perguntas em queries SQL.

Schema do banco PostgreSQL (Dataset Olist Brazilian E-Commerce):
Tabelas:
- customers: customer_id (PK), customer_unique_id, customer_zip_code_prefix, customer_city, customer_state
- orders: order_id (PK), customer_id (FK), order_status, order_purchase_timestamp
- order_items: order_id (FK), product_id (FK), order_item_id, price, freight_value
- products: product_id (PK), product_category_name, product_weight_g
- order_payments: order_id (FK), payment_type, payment_value
- product_embeddings: product_id (PK), category_name, text_content, embedding (vector)

Regras:
1. Use JOINs quando necessário para conectar tabelas.
2. Retorne APENAS a instrução SQL válida, sem blocos markdown ou explicações.
3. Para buscar por similaridade vetorial na tabela `product_embeddings`, use a sintaxe do pgvector: `ORDER BY embedding <=> :vector LIMIT 5`.
4. Para métricas financeiras: Receita = SUM(price + freight_value).

Pergunta: {input}"""

        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

        return prompt | self.llm | StrOutputParser()

    def _create_response_chain(self):
        """Cria a chain de resposta usando LCEL."""
        system_prompt = """Você é um assistente sênior de BI e Ciência de Dados. Formate os resultados de forma clara e profissional.

Pergunta: {pergunta}
SQL: {sql}
Resultados: {resultados}

Responda em português, destacando números e insights relevantes. Se não houver dados, informe isso educadamente."""

        prompt = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("human", "Formate a resposta.")]
        )

        return prompt | self.llm | StrOutputParser()

    def _clean_sql(self, sql: str) -> str:
        """Limpa a query SQL gerada."""
        sql = re.sub(r"```sql\s*", "", sql)
        sql = re.sub(r"```\s*", "", sql)
        sql = " ".join(sql.split())
        if sql.endswith(";"):
            sql = sql[:-1]
        return sql.strip()

    def generate_sql(self, pergunta: str) -> str:
        """Gera SQL a partir da pergunta do usuário."""
        try:
            logger.info(f"Gerando SQL para: {pergunta}")
            result = self.sql_chain.invoke({"input": pergunta})
            return self._clean_sql(result)
        except Exception as e:
            logger.error(f"Erro ao gerar SQL: {str(e)}")
            raise

    def vector_semantic_search(
        self, query_text: str, db: Session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executa busca por similaridade semântica via pgvector.
        """
        from ai.embed_products import generate_embedding

        query_vector = generate_embedding(query_text)
        vector_str = f"[{','.join(map(str, query_vector))}]"

        sql_query = text("""
            SELECT product_id, category_name, text_content,
                   (embedding <=> :query_vector::vector) as distance
            FROM product_embeddings
            ORDER BY embedding <=> :query_vector::vector
            LIMIT :limit
        """)

        result = db.execute(sql_query, {"query_vector": vector_str, "limit": limit})
        items = []
        for row in result:
            items.append(
                {
                    "product_id": row.product_id,
                    "category_name": row.category_name,
                    "text_content": row.text_content,
                    "similarity_score": (
                        round(1.0 - float(row.distance), 4) if row.distance is not None else 1.0
                    ),
                }
            )
        return items

    def format_response(self, pergunta: str, sql: str, resultados: Any) -> str:
        """Formata a resposta em linguagem natural."""
        try:
            resultados_str = str(resultados[:5] if isinstance(resultados, list) else resultados)
            if len(resultados_str) > 1500:
                resultados_str = resultados_str[:1500] + "..."

            return self.response_chain.invoke(
                {
                    "pergunta": pergunta,
                    "sql": sql or "N/A (Busca Semântica Vectorial)",
                    "resultados": resultados_str,
                }
            ).strip()
        except Exception as e:
            logger.error(f"Erro ao formatar resposta: {str(e)}")
            return f"Resultados obtidos: {resultados}"
