"""
Repository para operações com orders.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date, datetime
from backend.models.order import Order
from backend.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository para operações específicas de orders.
    """
    
    def __init__(self, db: Session):
        super().__init__(Order, db)
    
    def get_by_customer_id(self, customer_id: str) -> List[Order]:
        """
        Busca pedidos de um cliente.
        
        Args:
            customer_id: ID do cliente
            
        Returns:
            Lista de pedidos do cliente
        """
        return self.db.query(Order).filter(Order.customer_id == customer_id).all()
    
    def get_by_status(self, status: str) -> List[Order]:
        """
        Busca pedidos por status.
        
        Args:
            status: Status do pedido
            
        Returns:
            Lista de pedidos com o status
        """
        return self.db.query(Order).filter(Order.order_status == status).all()
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Order]:
        """
        Busca pedidos em um período de datas.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            
        Returns:
            Lista de pedidos no período
        """
        return self.db.query(Order).filter(
            Order.order_purchase_timestamp >= start_date,
            Order.order_purchase_timestamp <= end_date
        ).all()
    
    def get_delivered_orders(self) -> List[Order]:
        """
        Busca pedidos entregues.
        
        Returns:
            Lista de pedidos com status 'delivered'
        """
        return self.db.query(Order).filter(Order.order_status == 'delivered').all()
