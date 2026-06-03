"""
Módulo de extração de dados dos CSVs do dataset Olist.
"""
import pandas as pd
from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)


def extract_olist_csvs(data_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Extrai dados dos 5 arquivos CSV principais do dataset Olist.
    
    Args:
        data_dir: Diretório onde estão os CSVs
        
    Returns:
        Dicionário com nome da tabela e DataFrame correspondente
        
    Raises:
        FileNotFoundError: Se algum arquivo não existir
    """
    data_path = Path(data_dir)
    
    # Arquivos CSV principais do Olist
    csv_files = {
        'customers': 'olist_customers_dataset.csv',
        'orders': 'olist_orders_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'order_payments': 'olist_order_payments_dataset.csv'
    }
    
    dataframes = {}
    
    for table_name, filename in csv_files.items():
        file_path = data_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        logger.info(f"Extraindo dados de {filename}...")
        df = pd.read_csv(file_path)
        dataframes[table_name] = df
        logger.info(f"  {table_name}: {len(df)} registros, {len(df.columns)} colunas")
    
    return dataframes


def extract_single_csv(file_path: str) -> pd.DataFrame:
    """
    Extrai dados de um único arquivo CSV.
    
    Args:
        file_path: Caminho do arquivo CSV
        
    Returns:
        DataFrame com os dados extraídos
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    if not path.suffix.lower() == '.csv':
        raise ValueError(f"Arquivo deve ser CSV: {file_path}")
    
    logger.info(f"Extraindo dados de {file_path}...")
    df = pd.read_csv(file_path)
    logger.info(f"  {len(df)} registros, {len(df.columns)} colunas")
    
    return df
