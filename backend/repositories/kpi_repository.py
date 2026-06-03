"""
Repository para consultas analíticas e KPIs do dataset Olist.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, extract
from decimal import Decimal
from datetime import date

from backend.models.customer import Customer
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.order_payment import OrderPayment
from backend.models.product import Product


class KPIRepository:
    """
    Repository para consultas analíticas complexas e cálculo de KPIs.
    
    Centraliza todas as queries de negócio para o dataset Olist.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o repository de KPIs.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
    
    def get_receita_total(self) -> Decimal:
        """
        Calcula a receita total (soma de price + freight_value de order_items).
        
        Returns:
            Receita total
        """
        result = self.db.query(
            func.sum(OrderItem.price + OrderItem.freight_value)
        ).scalar()
        return result or Decimal('0')
    
    def get_numero_pedidos(self) -> int:
        """
        Calcula o número total de pedidos.
        
        Returns:
            Número total de pedidos
        """
        return self.db.query(func.count(Order.order_id)).scalar() or 0
    
    def get_clientes_unicos(self) -> int:
        """
        Calcula o número de clientes únicos.
        
        Returns:
            Número de clientes únicos
        """
        return self.db.query(func.count(Customer.customer_id.distinct())).scalar() or 0
    
    def get_ticket_medio(self) -> Decimal:
        """
        Calcula o ticket médio (receita total / número de pedidos).
        
        Returns:
            Ticket médio
        """
        receita_total = self.get_receita_total()
        numero_pedidos = self.get_numero_pedidos()
        
        if numero_pedidos == 0:
            return Decimal('0')
        
        return receita_total / numero_pedidos
    
    def get_receita_por_estado(self) -> List[Dict[str, Any]]:
        """
        Calcula a receita por estado.
        
        Returns:
            Lista de dicionários com estado e receita
        """
        results = (
            self.db.query(
                Customer.customer_state,
                func.sum(OrderItem.price + OrderItem.freight_value).label('receita')
            )
            .join(Order, Customer.customer_id == Order.customer_id)
            .join(OrderItem, Order.order_id == OrderItem.order_id)
            .group_by(Customer.customer_state)
            .order_by(desc('receita'))
            .all()
        )
        
        return [
            {'estado': r[0], 'receita': r[1]}
            for r in results
        ]
    
    def get_receita_por_mes(self) -> List[Dict[str, Any]]:
        """
        Calcula a receita por mês.
        
        Returns:
            Lista de dicionários com ano, mês e receita
        """
        results = (
            self.db.query(
                extract('year', Order.order_purchase_timestamp).label('ano'),
                extract('month', Order.order_purchase_timestamp).label('mes'),
                func.sum(OrderItem.price + OrderItem.freight_value).label('receita')
            )
            .join(OrderItem, Order.order_id == OrderItem.order_id)
            .group_by('ano', 'mes')
            .order_by('ano', 'mes')
            .all()
        )
        
        return [
            {'ano': int(r[0]), 'mes': int(r[1]), 'receita': r[2]}
            for r in results
        ]
    
    def get_top_produtos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna os top produtos por faturamento.
        
        Args:
            limit: Quantidade máxima de produtos
            
        Returns:
            Lista de dicionários com produto e faturamento
        """
        results = (
            self.db.query(
                Product.product_id,
                Product.product_category_name,
                func.sum(OrderItem.price).label('faturamento'),
                func.sum(OrderItem.price + OrderItem.freight_value).label('receita_total'),
                func.count(OrderItem.order_id).label('quantidade')
            )
            .join(OrderItem, Product.product_id == OrderItem.product_id)
            .group_by(Product.product_id, Product.product_category_name)
            .order_by(desc('faturamento'))
            .limit(limit)
            .all()
        )
        
        return [
            {
                'product_id': r[0],
                'categoria': r[1],
                'faturamento': r[2],
                'receita_total': r[3],
                'quantidade': r[4]
            }
            for r in results
        ]
    
    def get_top_categorias(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna as top categorias por faturamento.
        
        Args:
            limit: Quantidade máxima de categorias
            
        Returns:
            Lista de dicionários com categoria e faturamento
        """
        results = (
            self.db.query(
                Product.product_category_name,
                func.sum(OrderItem.price).label('faturamento'),
                func.sum(OrderItem.price + OrderItem.freight_value).label('receita_total'),
                func.count(OrderItem.order_id).label('quantidade')
            )
            .join(OrderItem, Product.product_id == OrderItem.product_id)
            .group_by(Product.product_category_name)
            .order_by(desc('faturamento'))
            .limit(limit)
            .all()
        )
        
        return [
            {
                'categoria': r[0],
                'faturamento': r[1],
                'receita_total': r[2],
                'quantidade': r[3]
            }
            for r in results if r[0]
        ]
    
    def get_metodos_pagamento(self) -> List[Dict[str, Any]]:
        """
        Retorna a distribuição por método de pagamento.
        
        Returns:
            Lista de dicionários com tipo, quantidade e valor
        """
        results = (
            self.db.query(
                OrderPayment.payment_type,
                func.count(OrderPayment.order_id).label('quantidade'),
                func.sum(OrderPayment.payment_value).label('valor_total')
            )
            .group_by(OrderPayment.payment_type)
            .order_by(desc('valor_total'))
            .all()
        )
        
        return [
            {
                'tipo': r[0],
                'quantidade': r[1],
                'valor_total': r[2]
            }
            for r in results
        ]
    
    def get_pedidos_por_estado(self) -> List[Dict[str, Any]]:
        """
        Retorna a quantidade de pedidos por estado.
        
        Returns:
            Lista de dicionários com estado e quantidade de pedidos
        """
        results = (
            self.db.query(
                Customer.customer_state,
                func.count(Order.order_id).label('quantidade')
            )
            .join(Order, Customer.customer_id == Order.customer_id)
            .group_by(Customer.customer_state)
            .order_by(desc('quantidade'))
            .all()
        )
        
        return [
            {'estado': r[0], 'quantidade': r[1]}
            for r in results
        ]
    
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
