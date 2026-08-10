"""
Configuração de conexão com o banco de dados PostgreSQL / SQLite.
Dataset Olist Brazilian E-Commerce.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# URL padrão do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vendas_user:vendas_password@localhost:5432/vendas_db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DATABASE_URL_PG = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://") if "postgresql+pg8000" not in DATABASE_URL else DATABASE_URL
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        res = sock.connect_ex(('localhost', 5432))
        sock.close()
        if res != 0:
            raise ConnectionError("PostgreSQL não acessível em localhost:5432")
        test_engine = create_engine(DATABASE_URL_PG, pool_pre_ping=True)
        with test_engine.connect() as conn:
            pass
        engine = test_engine
    except Exception:
        # Fallback para SQLite em desenvolvimento local sem container ativo
        engine = create_engine("sqlite:///./olist.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency para obter sessão do banco de dados nos endpoints FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa o banco de dados criando todas as tabelas e índices de alta performance."""
    from backend.models import Customer, Product, Order, OrderItem, OrderPayment, ProductEmbedding
    from sqlalchemy import text

    Base.metadata.create_all(bind=engine)
    
    # Cria índices otimizados em SQL puro para acelerar agrupamentos e joins
    with engine.begin() as conn:
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_customers_state ON customers(customer_state);'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_orders_purchase_time ON orders(order_purchase_timestamp);'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_order_payments_order_id ON order_payments(order_id);'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_order_payments_type ON order_payments(payment_type);'))

