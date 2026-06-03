"""
Modelo SQLAlchemy para a tabela order_items do dataset Olist.
"""
from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


class OrderItem(Base):
    """
    Modelo representando um item de pedido.
    
    Baseado no dataset Olist: olist_order_items_dataset.csv
    
    Chave primária composta: (order_id, order_item_id)
    
    Atributos:
        order_id: Chave estrangeira para orders
        order_item_id: Número sequencial do item no pedido
        product_id: Chave estrangeira para products
        seller_id: Identificador do vendedor
        shipping_limit_date: Data limite de envio
        price: Preço do item
        freight_value: Valor do frete
    """
    __tablename__ = "order_items"
    
    order_id = Column(String(50), ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False, index=True)
    seller_id = Column(String(50), index=True)
    shipping_limit_date = Column(Date, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    freight_value = Column(Numeric(10, 2), nullable=False)
    
    # Relacionamentos
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(order_id='{self.order_id}', item_id={self.order_item_id}, product_id='{self.product_id}')>"
