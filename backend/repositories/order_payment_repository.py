"""
Repository para operações com order_payments.
"""
from typing import List
from sqlalchemy.orm import Session
from backend.models.order_payment import OrderPayment
from backend.repositories.base import BaseRepository


class OrderPaymentRepository(BaseRepository[OrderPayment]):
    """
    Repository para operações específicas de order_payments.
    """
    
    def __init__(self, db: Session):
        super().__init__(OrderPayment, db)
    
    def get_by_order_id(self, order_id: str) -> List[OrderPayment]:
        """
        Busca pagamentos de um pedido.
        
        Args:
            order_id: ID do pedido
            
        Returns:
            Lista de pagamentos do pedido
        """
        return self.db.query(OrderPayment).filter(OrderPayment.order_id == order_id).all()
    
    def get_by_payment_type(self, payment_type: str) -> List[OrderPayment]:
        """
        Busca pagamentos por tipo.
        
        Args:
            payment_type: Tipo de pagamento (credit_card, boleto, voucher, debit_card)
            
        Returns:
            Lista de pagamentos do tipo
        """
        return self.db.query(OrderPayment).filter(OrderPayment.payment_type == payment_type).all()
