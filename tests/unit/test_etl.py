"""
Testes unitários para o módulo ETL.
"""
import pytest
import pandas as pd
from datetime import datetime
from etl.transform import (
    validate_columns,
    validate_data_types,
    validate_business_rules,
    standardize_text,
    calculate_faturamento,
    transform
)


def test_validate_columns_sucesso():
    """Testa validação de colunas com DataFrame válido."""
    df = pd.DataFrame({
        'id_venda': ['1', '2'],
        'data_venda': ['2024-01-01', '2024-01-02'],
        'produto': ['Produto A', 'Produto B'],
        'categoria': ['Cat A', 'Cat B'],
        'cidade': ['São Paulo', 'Rio de Janeiro'],
        'quantidade': [10, 20],
        'valor_unitario': [100.0, 200.0]
    })
    
    valido, erros = validate_columns(df)
    assert valido is True
    assert len(erros) == 0


def test_validate_columns_falha():
    """Testa validação de colunas com DataFrame inválido."""
    df = pd.DataFrame({
        'id_venda': ['1', '2'],
        'produto': ['Produto A', 'Produto B']
    })
    
    valido, erros = validate_columns(df)
    assert valido is False
    assert len(erros) > 0


def test_calculate_faturamento():
    """Testa cálculo de faturamento."""
    df = pd.DataFrame({
        'quantidade': [10, 20],
        'valor_unitario': [100.0, 200.0]
    })
    
    resultado = calculate_faturamento(df)
    assert 'faturamento' in resultado.columns
    assert resultado['faturamento'].iloc[0] == 1000.0
    assert resultado['faturamento'].iloc[1] == 4000.0


def test_standardize_text():
    """Testa padronização de texto."""
    df = pd.DataFrame({
        'produto': ['  produto a  ', 'PRODUTO B'],
        'categoria': ['  categoria a  ', 'CATEGORIA B'],
        'cidade': ['  são paulo  ', 'RIO DE JANEIRO']
    })
    
    resultado = standardize_text(df)
    assert resultado['produto'].iloc[0] == 'Produto A'
    assert resultado['cidade'].iloc[1] == 'Rio De Janeiro'


def test_validate_business_rules():
    """Testa validação de regras de negócio."""
    df = pd.DataFrame({
        'id_venda': ['1', '2', '3', '4'],
        'data_venda': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']),
        'produto': ['A', 'B', 'C', 'D'],
        'categoria': ['X', 'Y', 'Z', 'W'],
        'cidade': ['SP', 'RJ', 'MG', 'RS'],
        'quantidade': [10, -5, 20, 30],  # -5 deve ser removido
        'valor_unitario': [100.0, 200.0, -50.0, 300.0]  # -50.0 deve ser removido
    })
    
    resultado, avisos = validate_business_rules(df)
    assert len(resultado) < len(df)  # Alguns registros devem ser removidos
    assert len(avisos) > 0


def test_transform_pipeline_completo():
    """Testa pipeline completo de transformação."""
    df = pd.DataFrame({
        'id_venda': ['1', '2', '3'],
        'data_venda': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'produto': ['produto a', 'PRODUTO B', 'Produto C'],
        'categoria': ['cat a', 'CAT B', 'Cat C'],
        'cidade': ['são paulo', 'RIO DE JANEIRO', 'Belo Horizonte'],
        'quantidade': [10, 20, 30],
        'valor_unitario': [100.0, 200.0, 300.0]
    })
    
    resultado, erros, avisos = transform(df)
    
    assert len(resultado) == 3
    assert 'faturamento' in resultado.columns
    assert resultado['faturamento'].iloc[0] == 1000.0
    assert resultado['produto'].iloc[0] == 'Produto A'
    assert resultado['cidade'].iloc[1] == 'Rio De Janeiro'
