"""
Modelo SQLAlchemy para a tabela orders do dataset Olist.
"""
from sqlalchemy import Column, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


class Order(Base):
    """
    Modelo representando um pedido.
    
    Baseado no dataset Olist: olist_orders_dataset.csv
    
    Atributos:
        order_id: Chave primária, identificador único do pedido
        customer_id: Chave estrangeira para customers
        order_status: Status do pedido (created, approved, delivered, etc.)
        order_purchase_timestamp: Data/hora da compra
        order_approved_at: Data/hora da aprovação
        order_delivered_carrier_date: Data/hora de entrega ao transportador
        order_delivered_customer_date: Data/hora de entrega ao cliente
        order_estimated_delivery_date: Data estimada de entrega
    """
    __tablename__ = "orders"
    
    order_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    order_status = Column(String(20), nullable=False, index=True)
    order_purchase_timestamp = Column(DateTime, nullable=False, index=True)
    order_approved_at = Column(DateTime)
    order_delivered_carrier_date = Column(DateTime)
    order_delivered_customer_date = Column(DateTime)
    order_estimated_delivery_date = Column(Date, nullable=False, index=True)
    
    # Relacionamentos
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    order_payments = relationship("OrderPayment", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(order_id='{self.order_id}', status='{self.order_status}', customer_id='{self.customer_id}')>"
