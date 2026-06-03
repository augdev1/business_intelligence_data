"""
Serviço de negócio para cálculo de indicadores.
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import date
import logging

from backend.repositories.venda_repository import VendaRepository

logger = logging.getLogger(__name__)


class IndicadorService:
    """
    Serviço para cálculo de indicadores de negócio.
    
    Centraliza todos os cálculos de KPIs e métricas.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de indicadores.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = VendaRepository(db)
    
    def calcular_todos_indicadores(self) -> Dict[str, Any]:
        """
        Calcula todos os indicadores de negócio.
        
        Returns:
            Dicionário com todos os indicadores calculados
        """
        logger.info("Calculando todos os indicadores")
        
        return {
            'faturamento_total': self.repository.get_faturamento_total(),
            'quantidade_total': self.repository.get_quantidade_total(),
            'ticket_medio': self.repository.get_ticket_medio(),
            'produto_mais_vendido': self.repository.get_produto_mais_vendido(),
            'categoria_mais_vendida': self.repository.get_categoria_mais_vendida(),
            'cidade_maior_faturamento': self.repository.get_cidade_maior_faturamento(),
            'evolucao_mensal': self.repository.get_evolucao_mensal(),
            'ranking_produtos': self.repository.get_ranking_produtos(limit=10),
            'ranking_cidades': self.repository.get_ranking_cidades(limit=10),
            'total_vendas': self.repository.count()
        }
    
    def get_faturamento_total(self) -> float:
        """
        Retorna o faturamento total.
        
        Returns:
            Faturamento total
        """
        return float(self.repository.get_faturamento_total())
    
    def get_quantidade_total(self) -> int:
        """
        Retorna a quantidade total vendida.
        
        Returns:
            Quantidade total
        """
        return self.repository.get_quantidade_total()
    
    def get_ticket_medio(self) -> float:
        """
        Retorna o ticket médio.
        
        Returns:
            Ticket médio
        """
        return float(self.repository.get_ticket_medio())
    
    def get_evolucao_mensal(self) -> List[Dict[str, Any]]:
        """
        Retorna a evolução mensal das vendas.
        
        Returns:
            Lista de dados mensais
        """
        return self.repository.get_evolucao_mensal()
    
    def get_ranking_produtos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna o ranking de produtos.
        
        Args:
            limit: Quantidade máxima de produtos
            
        Returns:
            Lista de produtos no ranking
        """
        return self.repository.get_ranking_produtos(limit=limit)
    
    def get_ranking_cidades(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna o ranking de cidades.
        
        Args:
            limit: Quantidade máxima de cidades
            
        Returns:
            Lista de cidades no ranking
        """
        return self.repository.get_ranking_cidades(limit=limit)
    
    def get_vendas_por_periodo(
        self, data_inicio: date, data_fim: date
    ) -> List[Any]:
        """
        Retorna vendas em um período específico.
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            Lista de vendas no período
        """
        return self.repository.get_vendas_por_periodo(data_inicio, data_fim)
