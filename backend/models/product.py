"""
Modelo SQLAlchemy para a tabela products do dataset Olist.
"""
from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from database.connection import Base


class Product(Base):
    """
    Modelo representando um produto.
    
    Baseado no dataset Olist: olist_products_dataset.csv
    
    Atributos:
        product_id: Chave primária, identificador único do produto
        product_category_name: Categoria do produto (em português)
        product_name_lenght: Comprimento do nome do produto
        product_description_lenght: Comprimento da descrição
        product_photos_qty: Quantidade de fotos
        product_weight_g: Peso do produto em gramas
        product_length_cm: Comprimento em cm
        product_height_cm: Altura em cm
        product_width_cm: Largura em cm
    """
    __tablename__ = "products"
    
    product_id = Column(String(50), primary_key=True, index=True)
    product_category_name = Column(String(100), index=True)
    product_name_lenght = Column(Numeric(10, 2))
    product_description_lenght = Column(Numeric(10, 2))
    product_photos_qty = Column(Numeric(10, 2))
    product_weight_g = Column(Numeric(10, 2))
    product_length_cm = Column(Numeric(10, 2))
    product_height_cm = Column(Numeric(10, 2))
    product_width_cm = Column(Numeric(10, 2))
    
    # Relacionamento com order_items
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(product_id='{self.product_id}', category='{self.product_category_name}')>"
