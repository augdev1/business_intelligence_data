"""
Configuração de fixtures para testes.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import Base
from backend.models.venda import Venda


# Database de teste
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture
def test_engine():
    """Cria engine de banco de dados para testes."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db(test_engine):
    """Cria sessão de banco de dados para testes."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_venda_data():
    """Dados de venda de exemplo para testes."""
    return {
        'id_venda': 'TEST001',
        'data_venda': date(2024, 1, 1),
        'produto': 'Produto Teste',
        'categoria': 'Categoria Teste',
        'cidade': 'São Paulo',
        'quantidade': 10,
        'valor_unitario': Decimal('100.00'),
        'faturamento': Decimal('1000.00')
    }
