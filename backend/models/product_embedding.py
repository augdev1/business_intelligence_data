"""
Modelo SQLAlchemy para a tabela product_embeddings usando pgvector com fallback SQLite.
"""
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from database.connection import Base

try:
    from pgvector.sqlalchemy import Vector
    VectorType = Vector(1536)
except ImportError:
    VectorType = JSON


class ProductEmbedding(Base):
    """
    Tabela de embeddings de produtos para busca semântica via pgvector.
    
    Atributos:
        product_id: ID do produto (Primary Key / Foreign Key)
        category_name: Categoria do produto
        text_content: Conteúdo em texto concatenado (para busca e contexto)
        embedding: Vetor de embedding
    """
    __tablename__ = "product_embeddings"

    product_id = Column(String(50), primary_key=True, index=True)
    category_name = Column(String(100), index=True)
    text_content = Column(Text, nullable=False)
    embedding = Column(VectorType, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ProductEmbedding(product_id='{self.product_id}', category='{self.category_name}')>"
