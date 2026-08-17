"""
Serviço RAG (Retrieval-Augmented Generation) para integração com a API FastAPI.
"""

import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ai.sql_chain import SQLChain

logger = logging.getLogger(__name__)


class RAGService:
    """
    Camada de serviço para execução de RAG Híbrido e consultas semânticas vetoriais.
    """

    def __init__(self, ai_provider: str = "groq"):
        self.ai_provider = ai_provider
        self._chain = None

    @property
    def chain(self) -> SQLChain:
        if self._chain is None:
            try:
                self._chain = SQLChain(ai_provider=self.ai_provider)
            except Exception as e:
                logger.warning(f"Erro ao carregar SQLChain com provider {self.ai_provider}: {e}")
                self._chain = None
        return self._chain

    def process_rag_query(self, pergunta: str, db: Session) -> Dict[str, Any]:
        """
        Processa uma pergunta via RAG Híbrido, combinando busca vetorial e SQL.
        """
        if self.chain:
            return self.chain.rag_hybrid_query(pergunta, db)

        # Fallback sem LLM ativo
        return {
            "pergunta": pergunta,
            "resposta": f"Processamento local RAG para: '{pergunta}'. Modos vetoriais prontos.",
            "mode": "fallback_local",
            "sql": None,
            "sql_results": [],
            "reviews_evidences": [],
            "products_evidences": [],
        }

    def search_reviews_semantic(
        self, query: str, db: Session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca semântica dedicada em avaliações de clientes.
        """
        if self.chain:
            return self.chain.vector_review_search(query, db, limit=limit)
        return []

    def search_products_semantic(
        self, query: str, db: Session, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca semântica dedicada no catálogo de produtos.
        """
        if self.chain:
            return self.chain.vector_semantic_search(query, db, limit=limit)
        return []
