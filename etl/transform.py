"""
Módulo de transformação e validação de dados.
"""
import pandas as pd
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


# Colunas esperadas no CSV
COLUNAS_OBRIGATORIAS = [
    'id_venda',
    'data_venda',
    'produto',
    'categoria',
    'cidade',
    'quantidade',
    'valor_unitario'
]


def validate_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valida se o DataFrame possui todas as colunas obrigatórias.
    
    Args:
        df: DataFrame a ser validado
        
    Returns:
        Tupla (é_valido, lista_de_erros)
    """
    erros = []
    colunas_faltantes = set(COLUNAS_OBRIGATORIAS) - set(df.columns)
    
    if colunas_faltantes:
        erros.append(f"Colunas faltantes: {', '.join(colunas_faltantes)}")
    
    return len(erros) == 0, erros


def validate_data_types(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Converte e valida os tipos de dados das colunas.
    
    Args:
        df: DataFrame a ser transformado
        
    Returns:
        Tupla (DataFrame transformado, lista de erros)
    """
    erros = []
    df = df.copy()
    
    try:
        # Converte id_venda para string
        df['id_venda'] = df['id_venda'].astype(str)
    except Exception as e:
        erros.append(f"Erro ao converter id_venda: {str(e)}")
    
    try:
        # Converte data_venda para datetime
        df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
        # Remove datas inválidas
        datas_invalidas = df['data_venda'].isna().sum()
        if datas_invalidas > 0:
            erros.append(f"{datas_invalidas} registros com datas inválidas removidas")
            df = df[df['data_venda'].notna()]
    except Exception as e:
        erros.append(f"Erro ao converter data_venda: {str(e)}")
    
    try:
        # Converte quantidade para inteiro
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
        df['quantidade'] = df['quantidade'].astype('Int64')
    except Exception as e:
        erros.append(f"Erro ao converter quantidade: {str(e)}")
    
    try:
        # Converte valor_unitario para decimal
        df['valor_unitario'] = pd.to_numeric(df['valor_unitario'], errors='coerce')
    except Exception as e:
        erros.append(f"Erro ao converter valor_unitario: {str(e)}")
    
    return df, erros


def validate_business_rules(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Aplica regras de negócio para validar os dados.
    
    Args:
        df: DataFrame a ser validado
        
    Returns:
        Tupla (DataFrame filtrado, lista de avisos)
    """
    avisos = []
    df = df.copy()
    total_inicial = len(df)
    
    # Remove registros com valores nulos em campos obrigatórios
    df = df.dropna(subset=COLUNAS_OBRIGATORIAS)
    removidos_nulos = total_inicial - len(df)
    if removidos_nulos > 0:
        avisos.append(f"{removidos_nulos} registros removidos por valores nulos")
    
    # Valida quantidade > 0
    df = df[df['quantidade'] > 0]
    removidos_quantidade = total_inicial - len(df) - removidos_nulos
    if removidos_quantidade > 0:
        avisos.append(f"{removidos_quantidade} registros removidos por quantidade <= 0")
    
    # Valida valor_unitario >= 0
    df = df[df['valor_unitario'] >= 0]
    removidos_valor = total_inicial - len(df) - removidos_nulos - removidos_quantidade
    if removidos_valor > 0:
        avisos.append(f"{removidos_valor} registros removidos por valor_unitario < 0")
    
    # Remove duplicatas por id_venda
    duplicatas = df['id_venda'].duplicated().sum()
    if duplicatas > 0:
        avisos.append(f"{duplicatas} registros duplicados removidos (baseado em id_venda)")
        df = df.drop_duplicates(subset=['id_venda'], keep='first')
    
    return df, avisos


def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza campos de texto (trim, case).
    
    Args:
        df: DataFrame a ser padronizado
        
    Returns:
        DataFrame com textos padronizados
    """
    df = df.copy()
    
    # Remove espaços em branco
    df['produto'] = df['produto'].str.strip()
    df['categoria'] = df['categoria'].str.strip()
    df['cidade'] = df['cidade'].str.strip()
    df['id_venda'] = df['id_venda'].str.strip()
    
    # Converte para title case (primeira letra maiúscula)
    df['produto'] = df['produto'].str.title()
    df['categoria'] = df['categoria'].str.title()
    df['cidade'] = df['cidade'].str.title()
    
    return df


def calculate_faturamento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a coluna faturamento (quantidade * valor_unitario).
    
    Args:
        df: DataFrame com quantidade e valor_unitario
        
    Returns:
        DataFrame com coluna faturamento adicionada
    """
    df = df.copy()
    df['faturamento'] = df['quantidade'] * df['valor_unitario']
    return df


def transform(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Aplica todo o pipeline de transformação nos dados.
    
    Args:
        df: DataFrame extraído do CSV
        
    Returns:
        Tupla (DataFrame transformado, erros, avisos)
    """
    erros = []
    avisos = []
    
    # 1. Valida colunas obrigatórias
    colunas_validas, colunas_erros = validate_columns(df)
    if not colunas_validas:
        return pd.DataFrame(), colunas_erros, []
    
    # 2. Converte tipos de dados
    df, tipos_erros = validate_data_types(df)
    erros.extend(tipos_erros)
    
    # 3. Aplica regras de negócio
    df, regras_avisos = validate_business_rules(df)
    avisos.extend(regras_avisos)
    
    # 4. Padroniza textos
    df = standardize_text(df)
    
    # 5. Calcula faturamento
    df = calculate_faturamento(df)
    
    # 6. Seleciona e ordena colunas finais
    colunas_finais = [
        'id_venda',
        'data_venda',
        'produto',
        'categoria',
        'cidade',
        'quantidade',
        'valor_unitario',
        'faturamento'
    ]
    df = df[colunas_finais]
    
    logger.info(f"Transformação concluída: {len(df)} registros válidos")
    
    return df, erros, avisos
