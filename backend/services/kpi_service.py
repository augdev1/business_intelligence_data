"""
Serviço de negócio para cálculo de KPIs do dataset Olist com In-Memory Cache.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import logging
import time

from backend.repositories.kpi_repository import KPIRepository

logger = logging.getLogger(__name__)

# Cache em memória global com TTL
_kpi_cache: Optional[Dict[str, Any]] = None
_kpi_cache_time: float = 0
CACHE_TTL_SECONDS = 300  # 5 minutos


class KPIService:
    """
    Serviço para cálculo de indicadores de negócio do dataset Olist.

    Centraliza todos os cálculos de KPIs e métricas com otimização de cache.
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de KPIs.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = KPIRepository(db)

    def calcular_todos_kpis(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Calcula todos os KPIs de negócio ou retorna do cache.

        Args:
            force_refresh: Força a atualização do cache

        Returns:
            Dicionário com todos os KPIs calculados
        """
        global _kpi_cache, _kpi_cache_time

        now = time.time()
        if (
            not force_refresh
            and _kpi_cache is not None
            and (now - _kpi_cache_time) < CACHE_TTL_SECONDS
        ):
            logger.info("Retornando KPIs do cache em memória (Instantâneo)")
            return _kpi_cache

        logger.info("Calculando todos os KPIs no banco de dados...")
        t0 = time.time()

        result = {
            "receita_total": self.repository.get_receita_total(),
            "numero_pedidos": self.repository.get_numero_pedidos(),
            "clientes_unicos": self.repository.get_clientes_unicos(),
            "ticket_medio": self.repository.get_ticket_medio(),
            "receita_por_estado": self.repository.get_receita_por_estado(),
            "receita_por_mes": self.repository.get_receita_por_mes(),
            "top_produtos": self.repository.get_top_produtos(limit=20),
            "top_categorias": self.repository.get_top_categorias(limit=20),
            "metodos_pagamento": self.repository.get_metodos_pagamento(),
            "pedidos_por_estado": self.repository.get_pedidos_por_estado(),
        }

        _kpi_cache = result
        _kpi_cache_time = now

        logger.info(f"KPIs calculados e armazenados em cache em {time.time() - t0:.2f}s")
        return result

    def get_receita_total(self) -> float:
        """Retorna a receita total."""
        return float(self.repository.get_receita_total())

    def get_numero_pedidos(self) -> int:
        """Retorna o número de pedidos."""
        return self.repository.get_numero_pedidos()

    def get_clientes_unicos(self) -> int:
        """Retorna o número de clientes únicos."""
        return self.repository.get_clientes_unicos()

    def get_ticket_medio(self) -> float:
        """Retorna o ticket médio."""
        return float(self.repository.get_ticket_medio())

    def get_receita_por_estado(self) -> List[Dict[str, Any]]:
        """Retorna a receita por estado."""
        return self.repository.get_receita_por_estado()

    def get_receita_por_mes(self) -> List[Dict[str, Any]]:
        """Retorna a receita por mês."""
        return self.repository.get_receita_por_mes()

    def get_top_produtos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna os top produtos."""
        return self.repository.get_top_produtos(limit=limit)

    def get_top_categorias(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna as top categorias."""
        return self.repository.get_top_categorias(limit=limit)

    def get_metodos_pagamento(self) -> List[Dict[str, Any]]:
        """Retorna os métodos de pagamento."""
        return self.repository.get_metodos_pagamento()

    def get_pedidos_por_estado(self) -> List[Dict[str, Any]]:
        """Retorna os pedidos por estado."""
        return self.repository.get_pedidos_por_estado()
