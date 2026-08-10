"""
Serviço de integração com IA para consultas relacionais (Text-to-SQL) e semânticas (pgvector).
Dataset Olist Brazilian E-Commerce.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
import logging
import os

from backend.repositories.kpi_repository import KPIRepository
from ai.sql_chain import SQLChain

logger = logging.getLogger(__name__)


class IAService:
    """
    Serviço para integração com IA com suporte a consultas relacionais e busca vetorial.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = KPIRepository(db)
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv(usecwd=True), override=True)
        self.ai_provider = os.getenv("AI_PROVIDER", "groq")

        try:
            self.sql_chain = SQLChain(ai_provider=self.ai_provider)
            logger.info(f"IA configurada com provider: {self.ai_provider}")
        except Exception as e:
            logger.error(f"Erro ao configurar IA: {str(e)}")
            self.sql_chain = None

    def perguntar(self, pergunta: str) -> Dict[str, Any]:
        """
        Processa uma pergunta em linguagem natural usando busca vetorial ou Text-to-SQL.
        """
        try:
            logger.info(f"Processando pergunta: {pergunta}")

            if not self.sql_chain:
                return {
                    "sucesso": False,
                    "pergunta": pergunta,
                    "resposta": "IA não configurada. Verifique as variáveis de ambiente.",
                    "sql": None,
                    "dados": None,
                }

            # Detecção de intenção de busca por similaridade semântica
            keywords_vetoriais = [
                "similar",
                "parecido",
                "semelhante",
                "recomendação",
                "vetor",
                "embedding",
            ]
            is_semantic_search = any(kw in pergunta.lower() for kw in keywords_vetoriais)

            if is_semantic_search:
                logger.info("Executando busca por similaridade semântica via pgvector...")
                resultados = self.sql_chain.vector_semantic_search(pergunta, self.db, limit=5)
                sql_executado = (
                    "SELECT * FROM product_embeddings ORDER BY embedding <=> :vector LIMIT 5;"
                )
                resposta = self.sql_chain.format_response(pergunta, sql_executado, resultados)

                return {
                    "sucesso": True,
                    "pergunta": pergunta,
                    "resposta": resposta,
                    "sql": sql_executado,
                    "dados": resultados,
                }

            # Caso padrão: Text-to-SQL Relacional
            sql = self.sql_chain.generate_sql(pergunta)

            try:
                resultados = self.repository.execute_raw_query(sql)
                logger.info(f"Query executada com sucesso: {len(resultados)} resultados")
            except Exception as e:
                logger.error(f"Erro ao executar SQL: {str(e)}")
                return {
                    "sucesso": False,
                    "pergunta": pergunta,
                    "resposta": f"Erro ao executar query: {str(e)}",
                    "sql": sql,
                    "dados": None,
                }

            resposta = self.sql_chain.format_response(pergunta, sql, resultados)

            return {
                "sucesso": True,
                "pergunta": pergunta,
                "resposta": resposta,
                "sql": sql,
                "dados": resultados,
            }

        except Exception as e:
            logger.error(f"Erro ao processar pergunta: {str(e)}")
            return {
                "sucesso": False,
                "pergunta": pergunta,
                "resposta": f"Erro ao processar pergunta: {str(e)}",
                "sql": None,
                "dados": None,
            }
