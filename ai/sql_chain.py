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
        system_prompt = """Você é um assistente sênior de BI e Ciência de Dados. Formate os resultados de forma clara, profissional e extremamente limpa.

IMPORTANTE: Apresente a resposta em texto simples e bem estruturado. Evite o uso excessivo de formatação em negrito (asteriscos '**') ou itálico. Caso precise destacar termos principais ou listas, faça de forma discreta e minimalista.

Pergunta: {pergunta}
SQL: {sql}
Resultados: {resultados}

Responda em português, destacando números e insights relevantes. Se não houver dados, informe isso de maneira educada."""

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

    def _vector_search_python_fallback(
        self, query_vector: List[float], records: List[Any], limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Busca por similaridade de cosseno ultrarrápida vetorizada com NumPy."""
        if not records:
            return []

        import json
        import numpy as np

        valid_records = []
        vectors = []

        q = np.array(query_vector, dtype=float)
        norm_q = np.linalg.norm(q)
        if norm_q > 0:
            q = q / norm_q

        for r in records:
            emb = r.embedding
            if emb is None:
                continue
            if isinstance(emb, str):
                try:
                    emb = json.loads(emb)
                except Exception:
                    continue
            if isinstance(emb, list) and len(emb) > 0:
                valid_records.append(r)
                vectors.append(emb)

        if not valid_records:
            return []

        try:
            mat = np.array(vectors, dtype=float)
            norms = np.linalg.norm(mat, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            mat_norm = mat / norms

            scores = np.dot(mat_norm, q)
            top_indices = np.argsort(scores)[-limit:][::-1]

            results = []
            for idx in top_indices:
                r = valid_records[idx]
                score_val = float(scores[idx])
                item = {
                    "similarity_score": round(score_val, 4),
                    "text_content": getattr(r, "text_content", ""),
                }
                if hasattr(r, "review_id"):
                    item.update({
                        "review_id": r.review_id,
                        "order_id": getattr(r, "order_id", None),
                        "score": getattr(r, "score", None),
                        "comment_text": getattr(r, "comment_text", None),
                    })
                elif hasattr(r, "product_id"):
                    item.update({
                        "product_id": r.product_id,
                        "category_name": getattr(r, "category_name", None),
                    })
                results.append(item)
            return results
        except Exception as e:
            logger.error(f"Erro no fallback vetorizado NumPy: {e}")
            return []

    def vector_semantic_search(
        self, query_text: str, db: Session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executa busca por similaridade semântica de produtos via pgvector com fallback em Python.
        """
        from ai.embed_products import generate_embedding

        query_vector = generate_embedding(query_text)
        vector_str = f"[{','.join(map(str, query_vector))}]"

        try:
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
        except Exception as e:
            logger.warning(f"Fallback pgvector para busca de produtos: {e}")
            from backend.models.product_embedding import ProductEmbedding

            all_products = db.query(ProductEmbedding).limit(1000).all()
            return self._vector_search_python_fallback(query_vector, all_products, limit=limit)

    def vector_review_search(
        self, query_text: str, db: Session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executa busca por similaridade semântica de avaliações de clientes via pgvector com fallback em Python.
        """
        from ai.embed_products import generate_embedding

        query_vector = generate_embedding(query_text)
        vector_str = f"[{','.join(map(str, query_vector))}]"

        try:
            sql_query = text("""
                SELECT review_id, order_id, score, comment_text, text_content,
                       (embedding <=> :query_vector::vector) as distance
                FROM review_embeddings
                ORDER BY embedding <=> :query_vector::vector
                LIMIT :limit
            """)
            result = db.execute(sql_query, {"query_vector": vector_str, "limit": limit})
            items = []
            for row in result:
                items.append(
                    {
                        "review_id": row.review_id,
                        "order_id": row.order_id,
                        "score": row.score,
                        "comment_text": row.comment_text,
                        "text_content": row.text_content,
                        "similarity_score": (
                            round(1.0 - float(row.distance), 4) if row.distance is not None else 1.0
                        ),
                    }
                )
            return items
        except Exception as e:
            logger.warning(f"Fallback pgvector para busca de reviews: {e}")
            from backend.models.review_embedding import ReviewEmbedding

            all_reviews = db.query(ReviewEmbedding).limit(1000).all()
            return self._vector_search_python_fallback(query_vector, all_reviews, limit=limit)



    def rag_hybrid_query(self, pergunta: str, db: Session) -> Dict[str, Any]:
        """
        Executa consulta RAG Híbrida: combina busca de vetores em reviews/produtos + geração Text-to-SQL.
        """
        import unicodedata

        def _normalize(text_str: str) -> str:
            return "".join(
                c for c in unicodedata.normalize("NFD", text_str.lower())
                if unicodedata.category(c) != "Mn"
            )

        norm_q = _normalize(pergunta)
        mode = "hybrid"
        reviews_context = []
        products_context = []
        sql = None
        sql_results = None

        review_stems = [
            "opinio", "comentar", "reclamac", "avaliac", "review", "nota",
            "atraso", "qualidad", "gostou", "elogio", "critica", "atendimento",
            "entrega", "satisfeit", "insatisfeit", "bom", "ruim", "pessim", "otim"
        ]

        product_stems = [
            "produto", "categoria", "item", "semelhant", "recomendac", "marca", "peso"
        ]

        is_review_intent = any(stem in norm_q for stem in review_stems)
        is_product_intent = any(stem in norm_q for stem in product_stems)

        if is_review_intent:
            reviews_context = self.vector_review_search(pergunta, db, limit=5)
            mode = "vector_rag"

        if is_product_intent:
            products_context = self.vector_semantic_search(pergunta, db, limit=5)
            if not is_review_intent:
                mode = "vector_products"

        # Tentar gerar SQL para consultas quantitativas ou híbridas
        if not is_review_intent:
            try:
                sql = self.generate_sql(pergunta)
                if sql and sql.strip().upper().startswith("SELECT"):
                    res = db.execute(text(sql))
                    sql_results = [dict(row._mapping) for row in res.fetchall()]
                else:
                    sql = None
            except Exception as e:
                logger.warning(f"Erro ao executar SQL no RAG Híbrido: {e}")
                sql_results = None

        # Sintetizar evidências recuperadas
        context_parts = []
        if reviews_context:
            context_parts.append("--- AVALIAÇÕES DE CLIENTES (RAG VETORIAL) ---")
            for r in reviews_context:
                score_str = f"Nota {r.get('score')}/5" if r.get('score') else "Sem nota"
                comment_str = r.get('comment_text') or r.get('text_content')
                context_parts.append(f"• {score_str}: {comment_str}")

        if products_context:
            context_parts.append("--- PRODUTOS ENCONTRADOS (BUSCA VETORIAL) ---")
            for p in products_context:
                context_parts.append(f"• Produto {p.get('product_id')} ({p.get('category_name')}): {p.get('text_content')}")

        if sql_results:
            context_parts.append("--- RESULTADOS ANALÍTICOS (BANCO DE DADOS / SQL) ---")
            context_parts.append(str(sql_results[:5]))

        final_context = "\n".join(context_parts) if context_parts else "Nenhum contexto vetorial retornado."
        formatted_answer = self.format_response(pergunta, sql or "Busca Semântica RAG Vetorial", final_context)

        return {
            "pergunta": pergunta,
            "resposta": formatted_answer,
            "mode": mode,
            "sql": sql,
            "sql_results": sql_results,
            "reviews_evidences": reviews_context,
            "products_evidences": products_context,
        }


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

