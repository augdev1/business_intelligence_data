"""
Repository específico para operações com vendas e cálculo de indicadores.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import date, datetime
from decimal import Decimal

from backend.models.venda import Venda
from backend.repositories.base import BaseRepository


class VendaRepository(BaseRepository[Venda]):
    """
    Repository para operações específicas de vendas.
    
    Extende o repository base com métodos para consultas analíticas
    e cálculo de indicadores de negócio.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o repository de vendas.
        
        Args:
            db: Sessão do banco de dados
        """
        super().__init__(Venda, db)
    
    def get_by_id_venda(self, id_venda: str) -> Optional[Venda]:
        """
        Busca uma venda pelo id_venda (identificador do CSV).
        
        Args:
            id_venda: Identificador único da venda
            
        Returns:
            Instância de Venda ou None
        """
        return self.db.query(Venda).filter(Venda.id_venda == id_venda).first()
    
    def create_many(self, vendas: List[Dict[str, Any]]) -> List[Venda]:
        """
        Cria múltiplas vendas em batch.
        
        Args:
            vendas: Lista de dicionários com dados das vendas
            
        Returns:
            Lista de instâncias de Venda criadas
        """
        db_objs = [Venda(**venda) for venda in vendas]
        self.db.add_all(db_objs)
        self.db.commit()
        for obj in db_objs:
            self.db.refresh(obj)
        return db_objs
    
    def get_faturamento_total(self) -> Decimal:
        """
        Calcula o faturamento total.
        
        Returns:
            Soma de todos os faturamentos
        """
        result = self.db.query(func.sum(Venda.faturamento)).scalar()
        return result or Decimal('0')
    
    def get_quantidade_total(self) -> int:
        """
        Calcula a quantidade total vendida.
        
        Returns:
            Soma de todas as quantidades
        """
        result = self.db.query(func.sum(Venda.quantidade)).scalar()
        return result or 0
    
    def get_ticket_medio(self) -> Decimal:
        """
        Calcula o ticket médio (faturamento total / quantidade de vendas).
        
        Returns:
            Ticket médio
        """
        faturamento_total = self.get_faturamento_total()
        total_vendas = self.count()
        if total_vendas == 0:
            return Decimal('0')
        return faturamento_total / total_vendas
    
    def get_produto_mais_vendido(self) -> Optional[Dict[str, Any]]:
        """
        Identifica o produto mais vendido (por quantidade).
        
        Returns:
            Dicionário com produto e quantidade ou None
        """
        result = (
            self.db.query(
                Venda.produto,
                func.sum(Venda.quantidade).label('total_quantidade')
            )
            .group_by(Venda.produto)
            .order_by(desc('total_quantidade'))
            .first()
        )
        if result:
            return {'produto': result[0], 'quantidade': result[1]}
        return None
    
    def get_categoria_mais_vendida(self) -> Optional[Dict[str, Any]]:
        """
        Identifica a categoria mais vendida (por quantidade).
        
        Returns:
            Dicionário com categoria e quantidade ou None
        """
        result = (
            self.db.query(
                Venda.categoria,
                func.sum(Venda.quantidade).label('total_quantidade')
            )
            .group_by(Venda.categoria)
            .order_by(desc('total_quantidade'))
            .first()
        )
        if result:
            return {'categoria': result[0], 'quantidade': result[1]}
        return None
    
    def get_cidade_maior_faturamento(self) -> Optional[Dict[str, Any]]:
        """
        Identifica a cidade com maior faturamento.
        
        Returns:
            Dicionário com cidade e faturamento ou None
        """
        result = (
            self.db.query(
                Venda.cidade,
                func.sum(Venda.faturamento).label('total_faturamento')
            )
            .group_by(Venda.cidade)
            .order_by(desc('total_faturamento'))
            .first()
        )
        if result:
            return {'cidade': result[0], 'faturamento': result[1]}
        return None
    
    def get_evolucao_mensal(self) -> List[Dict[str, Any]]:
        """
        Calcula a evolução mensal das vendas.
        
        Returns:
            Lista de dicionários com mês, ano, faturamento e quantidade
        """
        results = (
            self.db.query(
                func.extract('year', Venda.data_venda).label('ano'),
                func.extract('month', Venda.data_venda).label('mes'),
                func.sum(Venda.faturamento).label('faturamento'),
                func.sum(Venda.quantidade).label('quantidade')
            )
            .group_by('ano', 'mes')
            .order_by('ano', 'mes')
            .all()
        )
        return [
            {
                'ano': int(r[0]),
                'mes': int(r[1]),
                'faturamento': r[2],
                'quantidade': r[3]
            }
            for r in results
        ]
    
    def get_ranking_produtos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Gera ranking de produtos por faturamento.
        
        Args:
            limit: Quantidade máxima de produtos no ranking
            
        Returns:
            Lista de dicionários com produto, quantidade e faturamento
        """
        results = (
            self.db.query(
                Venda.produto,
                func.sum(Venda.quantidade).label('quantidade'),
                func.sum(Venda.faturamento).label('faturamento')
            )
            .group_by(Venda.produto)
            .order_by(desc('faturamento'))
            .limit(limit)
            .all()
        )
        return [
            {
                'produto': r[0],
                'quantidade': r[1],
                'faturamento': r[2]
            }
            for r in results
        ]
    
    def get_ranking_cidades(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Gera ranking de cidades por faturamento.
        
        Args:
            limit: Quantidade máxima de cidades no ranking
            
        Returns:
            Lista de dicionários com cidade, quantidade e faturamento
        """
        results = (
            self.db.query(
                Venda.cidade,
                func.sum(Venda.quantidade).label('quantidade'),
                func.sum(Venda.faturamento).label('faturamento')
            )
            .group_by(Venda.cidade)
            .order_by(desc('faturamento'))
            .limit(limit)
            .all()
        )
        return [
            {
                'cidade': r[0],
                'quantidade': r[1],
                'faturamento': r[2]
            }
            for r in results
        ]
    
    def get_vendas_por_periodo(
        self, data_inicio: date, data_fim: date
    ) -> List[Venda]:
        """
        Busca vendas em um período específico.
        
        Args:
            data_inicio: Data inicial do período
            data_fim: Data final do período
            
        Returns:
            Lista de vendas no período
        """
        return (
            self.db.query(Venda)
            .filter(
                and_(
                    Venda.data_venda >= data_inicio,
                    Venda.data_venda <= data_fim
                )
            )
            .all()
        )
    
    def execute_raw_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executa uma query SQL raw e retorna os resultados.
        
        Usado pelo assistente IA para executar queries geradas.
        
        Args:
            query: Query SQL a ser executada
            
        Returns:
            Lista de dicionários com os resultados
        """
        result = self.db.execute(query)
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
