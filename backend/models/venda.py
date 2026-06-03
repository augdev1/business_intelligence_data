"""
Modelo SQLAlchemy para a tabela de vendas.
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, CheckConstraint
from sqlalchemy.sql import func
from database.connection import Base


class Venda(Base):
    """
    Modelo representando uma venda.
    
    Atributos:
        id: Chave primária auto-incremento
        id_venda: Identificador único da venda (do CSV)
        data_venda: Data da venda
        produto: Nome do produto
        categoria: Categoria do produto
        cidade: Cidade da venda
        quantidade: Quantidade vendida (deve ser > 0)
        valor_unitario: Valor unitário (deve ser >= 0)
        faturamento: Valor total (quantidade * valor_unitario)
        created_at: Timestamp de criação
        updated_at: Timestamp de atualização
    """
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_venda = Column(String(50), unique=True, nullable=False, index=True)
    data_venda = Column(Date, nullable=False, index=True)
    produto = Column(String(255), nullable=False, index=True)
    categoria = Column(String(100), nullable=False, index=True)
    cidade = Column(String(100), nullable=False, index=True)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Numeric(10, 2), nullable=False)
    faturamento = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('quantidade > 0', name='ck_quantidade_positiva'),
        CheckConstraint('valor_unitario >= 0', name='ck_valor_unitario_nao_negativo'),
    )
    
    def __repr__(self):
        return f"<Venda(id_venda='{self.id_venda}', produto='{self.produto}', faturamento={self.faturamento})>"
