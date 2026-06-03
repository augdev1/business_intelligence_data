"""
Modelo SQLAlchemy para a tabela customers do dataset Olist.
"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.connection import Base


class Customer(Base):
    """
    Modelo representando um cliente.
    
    Baseado no dataset Olist: olist_customers_dataset.csv
    
    Atributos:
        customer_id: Chave primária, identificador único do cliente
        customer_unique_id: Identificador único agregado do cliente
        customer_zip_code_prefix: Prefixo do CEP
        customer_city: Cidade do cliente
        customer_state: Estado do cliente (UF)
    """
    __tablename__ = "customers"
    
    customer_id = Column(String(50), primary_key=True, index=True)
    customer_unique_id = Column(String(50), nullable=False, index=True)
    customer_zip_code_prefix = Column(Integer, nullable=False)
    customer_city = Column(String(100), nullable=False, index=True)
    customer_state = Column(String(2), nullable=False, index=True)
    
    # Relacionamento com orders
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Customer(customer_id='{self.customer_id}', city='{self.customer_city}', state='{self.customer_state}')>"
