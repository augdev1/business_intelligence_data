"""
Modelo SQLAlchemy para a tabela order_payments do dataset Olist.
"""
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


class OrderPayment(Base):
    """
    Modelo representando um pagamento de pedido.
    
    Baseado no dataset Olist: olist_order_payments_dataset.csv
    
    Chave primária composta: (order_id, payment_sequential)
    
    Atributos:
        order_id: Chave estrangeira para orders
        payment_sequential: Sequencial do pagamento
        payment_type: Tipo de pagamento (credit_card, boleto, voucher, debit_card)
        payment_installments: Número de parcelas
        payment_value: Valor do pagamento
    """
    __tablename__ = "order_payments"
    
    order_id = Column(String(50), ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String(20), nullable=False, index=True)
    payment_installments = Column(Integer, nullable=False)
    payment_value = Column(Numeric(10, 2), nullable=False)
    
    # Relacionamento
    order = relationship("Order", back_populates="order_payments")
    
    def __repr__(self):
        return f"<OrderPayment(order_id='{self.order_id}', type='{self.payment_type}', value={self.payment_value})>"
