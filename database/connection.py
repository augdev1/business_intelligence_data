"""
Configuração de conexão com o banco de dados PostgreSQL.
Dataset Olist Brazilian E-Commerce.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/olist_db")

# Engine do SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco de dados.
    Usada nos endpoints FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas do dataset Olist.
    Tabelas criadas:
    - customers
    - products
    - orders
    - order_items
    - order_payments
    """
    # Importa todos os modelos para garantir que sejam registrados no Base
    from backend.models import Customer, Product, Order, OrderItem, OrderPayment
    
    Base.metadata.create_all(bind=engine)
