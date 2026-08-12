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
        Processa uma pergunta em linguagem natural usando a engine RAG Híbrida.
        """
        try:
            logger.info(f"Processando pergunta via RAG Híbrido: {pergunta}")

            if not self.sql_chain:
                return {
                    "sucesso": False,
                    "pergunta": pergunta,
                    "resposta": "IA não configurada. Verifique as variáveis de ambiente (GROQ_API_KEY / OPENAI_API_KEY).",
                    "mode": "error",
                    "sql": None,
                    "dados": None,
                    "reviews_evidences": [],
                    "products_evidences": [],
                }

            rag_result = self.sql_chain.rag_hybrid_query(pergunta, self.db)

            return {
                "sucesso": True,
                "pergunta": pergunta,
                "resposta": rag_result.get("resposta", ""),
                "mode": rag_result.get("mode", "hybrid"),
                "sql": rag_result.get("sql"),
                "dados": rag_result.get("sql_results"),
                "reviews_evidences": rag_result.get("reviews_evidences"),
                "products_evidences": rag_result.get("products_evidences"),
            }

        except Exception as e:
            logger.error(f"Erro ao processar pergunta via RAG: {str(e)}")
            return {
                "sucesso": False,
                "pergunta": pergunta,
                "resposta": f"Erro ao processar pergunta: {str(e)}",
                "mode": "error",
                "sql": None,
                "dados": None,
                "reviews_evidences": [],
                "products_evidences": [],
            }

