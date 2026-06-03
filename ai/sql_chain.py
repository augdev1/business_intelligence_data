"""
Configuração do LangChain SQL chain para geração de queries.
Otimizado para performance usando LCEL (LangChain Expression Language).
"""
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import logging
import re

logger = logging.getLogger(__name__)


class SQLChain:
    """
    Chain para geração de SQL a partir de perguntas em linguagem natural.
    Otimizado com LCEL e cache para melhor performance.
    """
    
    def __init__(self, ai_provider: str = "openai"):
        """
        Inicializa a chain SQL.
        
        Args:
            ai_provider: Provider de IA ('openai' ou 'groq')
        """
        self.ai_provider = ai_provider
        self.llm = self._create_llm()
        self.sql_chain = self._create_sql_chain()
        self.response_chain = self._create_response_chain()
    
    def _create_llm(self):
        """
        Cria a instância do LLM baseado no provider configurado.
        Usa modelos otimizados para performance.
        
        Returns:
            Instância do LLM
        """
        if self.ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY não configurada")
            # gpt-4o-mini é mais rápido e barato que gpt-3.5-turbo
            return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                openai_api_key=api_key,
                max_tokens=500,
                timeout=30.0
            )
        elif self.ai_provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY não configurada")
            # Llama 3.3 70B - modelo mais recente
            return ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0,
                groq_api_key=api_key,
                max_tokens=500,
                timeout=30.0
            )
        else:
            raise ValueError(f"Provider não suportado: {self.ai_provider}")
    
    def _create_sql_chain(self):
        """
        Cria a chain SQL usando LCEL (LangChain Expression Language).
        LCEL é mais eficiente que LLMChain depreciado.
        
        Returns:
            Chain otimizada para geração de SQL
        """
        # Prompt otimizado e conciso para dataset Olist
        system_prompt = """Você é um especialista em SQL. Converta perguntas em queries SQL.

Schema do banco (Dataset Olist Brazilian E-Commerce):
Tabelas:
- customers: customer_id (PK), customer_unique_id, customer_city, customer_state
- orders: order_id (PK), customer_id (FK), order_status, order_purchase_timestamp
- order_items: order_id (FK), product_id (FK), order_item_id, price, freight_value
- products: product_id (PK), product_category_name
- order_payments: order_id (FK), payment_type, payment_value

Regras:
1. Use JOINs quando necessário para conectar tabelas
2. Retorne APENAS o SQL, sem explicações
3. Use SUM, COUNT, AVG quando apropriado
4. Use GROUP BY para agrupamentos
5. Use ORDER BY com DESC para rankings
6. Use LIMIT para top N resultados
7. Para receita: use SUM(price + freight_value)
8. Para ticket médio: SUM(price + freight_value) / COUNT(DISTINCT order_id)

Exemplos:
Pergunta: Qual estado gerou mais receita?
SQL: SELECT c.customer_state, SUM(oi.price + oi.freight_value) as receita FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_state ORDER BY receita DESC LIMIT 1;

Pergunta: Qual categoria teve maior receita?
SQL: SELECT p.product_category_name, SUM(oi.price) as receita FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_category_name ORDER BY receita DESC LIMIT 1;

Pergunta: Qual método de pagamento é mais utilizado?
SQL: SELECT payment_type, COUNT(*) as quantidade FROM order_payments GROUP BY payment_type ORDER BY quantidade DESC LIMIT 1;

Pergunta: {input}"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Chain LCEL otimizada
        chain = prompt | self.llm | StrOutputParser()
        return chain
    
    def _create_response_chain(self):
        """
        Cria a chain de resposta usando LCEL.
        
        Returns:
            Chain otimizada para formatação de resposta
        """
        system_prompt = """Você é um assistente de dados. Formate os resultados de forma clara e concisa.

Pergunta: {pergunta}
SQL: {sql}
Resultados: {resultados}

Responda em português, destacando os números principais. Se não houver dados, informe isso.
Não invente informações além dos dados fornecidos."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Formate a resposta.")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        return chain
    
    def _clean_sql(self, sql: str) -> str:
        """
        Limpa o SQL gerado removendo markdown e caracteres extras.
        
        Args:
            sql: SQL bruto
            
        Returns:
            SQL limpo
        """
        # Remove markdown code blocks
        sql = re.sub(r'```sql\s*', '', sql)
        sql = re.sub(r'```\s*', '', sql)
        
        # Remove espaços extras
        sql = ' '.join(sql.split())
        
        # Remove ponto final se presente
        if sql.endswith(';'):
            sql = sql[:-1]
        
        return sql.strip()
    
    def generate_sql(self, pergunta: str) -> str:
        """
        Gera SQL a partir de uma pergunta em linguagem natural.
        Usa LCEL otimizado com cache automático.
        
        Args:
            pergunta: Pergunta do usuário
            
        Returns:
            Query SQL gerada
        """
        try:
            logger.info(f"Gerando SQL para pergunta: {pergunta}")
            
            # Invoca chain LCEL (com cache automático)
            result = self.sql_chain.invoke({"input": pergunta})
            
            # Limpa o resultado
            sql = self._clean_sql(result)
            
            logger.info(f"SQL gerado: {sql}")
            return sql
            
        except Exception as e:
            logger.error(f"Erro ao gerar SQL: {str(e)}")
            raise
    
    def format_response(
        self, 
        pergunta: str, 
        sql: str, 
        resultados: Any
    ) -> str:
        """
        Formata os resultados em linguagem natural.
        Usa LCEL otimizado.
        
        Args:
            pergunta: Pergunta original
            sql: SQL executado
            resultados: Resultados da query
            
        Returns:
            Resposta em linguagem natural
        """
        try:
            # Converte resultados para string de forma eficiente
            if isinstance(resultados, list) and len(resultados) > 0:
                # Limita a 5 primeiros resultados para não exceder contexto
                resultados_limitados = resultados[:5] if len(resultados) > 5 else resultados
                resultados_str = str(resultados_limitados)
            else:
                resultados_str = str(resultados)
            
            # Limita tamanho total
            if len(resultados_str) > 1500:
                resultados_str = resultados_str[:1500] + "..."
            
            logger.info("Formatando resposta em linguagem natural")
            
            # Invoca chain LCEL
            resposta = self.response_chain.invoke({
                "pergunta": pergunta,
                "sql": sql,
                "resultados": resultados_str
            })
            
            return resposta.strip()
            
        except Exception as e:
            logger.error(f"Erro ao formatar resposta: {str(e)}")
            # Retorna resposta padrão em caso de erro
            return f"Baseado nos dados: {resultados}"
