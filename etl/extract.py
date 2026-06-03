"""
Módulo de extração de dados de arquivos CSV.
"""
import pandas as pd
from pathlib import Path
from typing import Optional


def extract_csv(file_path: str) -> pd.DataFrame:
    """
    Extrai dados de um arquivo CSV.
    
    Args:
        file_path: Caminho do arquivo CSV
        
    Returns:
        DataFrame com os dados extraídos
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        ValueError: Se o arquivo não for um CSV válido
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    if not path.suffix.lower() == '.csv':
        raise ValueError(f"Arquivo deve ser CSV: {file_path}")
    
    # Lê o CSV
    df = pd.read_csv(file_path)
    
    return df


def extract_csv_with_encoding(file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Extrai dados de um arquivo CSV com encoding específico.
    
    Útil para arquivos com caracteres especiais.
    
    Args:
        file_path: Caminho do arquivo CSV
        encoding: Encoding do arquivo (padrão: utf-8)
        
    Returns:
        DataFrame com os dados extraídos
    """
    df = pd.read_csv(file_path, encoding=encoding)
    return df
