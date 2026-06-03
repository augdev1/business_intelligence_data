"""
Testes unitários para serviços de negócio.
"""
import pytest
from unittest.mock import Mock, MagicMock
from datetime import date
from decimal import Decimal

from backend.services.indicador_service import IndicadorService


def test_indicador_service_get_faturamento_total():
    """Testa cálculo de faturamento total."""
    # Mock do banco de dados
    mock_db = Mock()
    mock_repository = Mock()
    mock_repository.get_faturamento_total.return_value = Decimal('10000.00')
    
    service = IndicadorService(mock_db)
    service.repository = mock_repository
    
    resultado = service.get_faturamento_total()
    
    assert resultado == 10000.0
    mock_repository.get_faturamento_total.assert_called_once()


def test_indicador_service_get_quantidade_total():
    """Testa cálculo de quantidade total."""
    mock_db = Mock()
    mock_repository = Mock()
    mock_repository.get_quantidade_total.return_value = 100
    
    service = IndicadorService(mock_db)
    service.repository = mock_repository
    
    resultado = service.get_quantidade_total()
    
    assert resultado == 100
    mock_repository.get_quantidade_total.assert_called_once()


def test_indicador_service_get_ticket_medio():
    """Testa cálculo de ticket médio."""
    mock_db = Mock()
    mock_repository = Mock()
    mock_repository.get_ticket_medio.return_value = Decimal('100.00')
    
    service = IndicadorService(mock_db)
    service.repository = mock_repository
    
    resultado = service.get_ticket_medio()
    
    assert resultado == 100.0
    mock_repository.get_ticket_medio.assert_called_once()


def test_indicador_service_get_ranking_produtos():
    """Testa obtenção de ranking de produtos."""
    mock_db = Mock()
    mock_repository = Mock()
    mock_repository.get_ranking_produtos.return_value = [
        {'produto': 'A', 'quantidade': 100, 'faturamento': 1000},
        {'produto': 'B', 'quantidade': 50, 'faturamento': 500}
    ]
    
    service = IndicadorService(mock_db)
    service.repository = mock_repository
    
    resultado = service.get_ranking_produtos(limit=5)
    
    assert len(resultado) == 2
    assert resultado[0]['produto'] == 'A'
    mock_repository.get_ranking_produtos.assert_called_once_with(limit=5)
