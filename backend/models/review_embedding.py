"""
Modelo SQLAlchemy para a tabela review_embeddings usando pgvector com fallback SQLite.
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON
from sqlalchemy.sql import func
from database.connection import Base

try:
    from pgvector.sqlalchemy import Vector
    VectorType = Vector(1536)
except ImportError:
    VectorType = JSON


class ReviewEmbedding(Base):
    """
    Tabela de embeddings de avaliações (reviews) para busca semântica de sentimento e RAG.

    Atributos:
        review_id: ID da avaliação (Primary Key)
        order_id: ID do pedido associado
        score: Nota da avaliação (1 a 5)
        category_name: Categoria do produto principal do pedido
        comment_text: Texto original do comentário
        text_content: Representação em texto enriquecida para geração de embedding
        embedding: Vetor de embedding de 1536 dimensões
    """
    __tablename__ = "review_embeddings"

    review_id = Column(String(50), primary_key=True, index=True)
    order_id = Column(String(50), index=True, nullable=True)
    score = Column(Integer, index=True, nullable=True)
    category_name = Column(String(100), index=True, nullable=True)
    comment_text = Column(Text, nullable=True)
    text_content = Column(Text, nullable=False)
    embedding = Column(VectorType, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ReviewEmbedding(review_id='{self.review_id}', score={self.score}, category='{self.category_name}')>"
