"""
Repository para operações com order_items.
"""
from typing import List
from sqlalchemy.orm import Session
from backend.models.order_item import OrderItem
from backend.repositories.base import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository para operações específicas de order_items.
    """
    
    def __init__(self, db: Session):
        super().__init__(OrderItem, db)
    
    def get_by_order_id(self, order_id: str) -> List[OrderItem]:
        """
        Busca itens de um pedido.
        
        Args:
            order_id: ID do pedido
            
        Returns:
            Lista de itens do pedido
        """
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    def get_by_product_id(self, product_id: str) -> List[OrderItem]:
        """
        Busca itens de um produto.
        
        Args:
            product_id: ID do produto
            
        Returns:
            Lista de itens do produto
        """
        return self.db.query(OrderItem).filter(OrderItem.product_id == product_id).all()
