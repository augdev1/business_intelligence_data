"""
Serviço de negócio para cálculo de KPIs do dataset Olist.
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
import logging

from backend.repositories.kpi_repository import KPIRepository

logger = logging.getLogger(__name__)


class KPIService:
    """
    Serviço para cálculo de indicadores de negócio do dataset Olist.
    
    Centraliza todos os cálculos de KPIs e métricas.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de KPIs.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = KPIRepository(db)
    
    def calcular_todos_kpis(self) -> Dict[str, Any]:
        """
        Calcula todos os KPIs de negócio.
        
        Returns:
            Dicionário com todos os KPIs calculados
        """
        logger.info("Calculando todos os KPIs")
        
        return {
            'receita_total': self.repository.get_receita_total(),
            'numero_pedidos': self.repository.get_numero_pedidos(),
            'clientes_unicos': self.repository.get_clientes_unicos(),
            'ticket_medio': self.repository.get_ticket_medio(),
            'receita_por_estado': self.repository.get_receita_por_estado(),
            'receita_por_mes': self.repository.get_receita_por_mes(),
            'top_produtos': self.repository.get_top_produtos(limit=10),
            'top_categorias': self.repository.get_top_categorias(limit=10),
            'metodos_pagamento': self.repository.get_metodos_pagamento(),
            'pedidos_por_estado': self.repository.get_pedidos_por_estado()
        }
    
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
