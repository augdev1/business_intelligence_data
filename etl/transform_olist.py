"""
Módulo de transformação e validação de dados do dataset Olist.
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


def transform_customers(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Transforma dados de customers.
    
    Args:
        df: DataFrame raw de customers
        
    Returns:
        Tupla (DataFrame transformado, erros, avisos)
    """
    erros = []
    avisos = []
    df = df.copy()
    
    # Remove duplicatas por customer_id
    duplicatas = df['customer_id'].duplicated().sum()
    if duplicatas > 0:
        avisos.append(f"{duplicatas} registros duplicados removidos (customer_id)")
        df = df.drop_duplicates(subset=['customer_id'], keep='first')
    
    # Valida campos obrigatórios
    campos_obrigatorios = ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']
    for campo in campos_obrigatorios:
        nulos = df[campo].isna().sum()
        if nulos > 0:
            avisos.append(f"{nulos} registros com {campo} nulo removidos")
            df = df[df[campo].notna()]
    
    # Converte tipos
    df['customer_zip_code_prefix'] = df['customer_zip_code_prefix'].astype(int)
    
    # Padroniza texto
    df['customer_city'] = df['customer_city'].str.strip().str.title()
    df['customer_state'] = df['customer_state'].str.strip().str.upper()
    
    logger.info(f"Customers transformados: {len(df)} registros")
    
    return df, erros, avisos


def transform_orders(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Transforma dados de orders.
    
    Args:
        df: DataFrame raw de orders
        
    Returns:
        Tupla (DataFrame transformado, erros, avisos)
    """
    erros = []
    avisos = []
    df = df.copy()
    
    # Remove duplicatas por order_id
    duplicatas = df['order_id'].duplicated().sum()
    if duplicatas > 0:
        avisos.append(f"{duplicatas} registros duplicados removidos (order_id)")
        df = df.drop_duplicates(subset=['order_id'], keep='first')
    
    # Valida campos obrigatórios
    campos_obrigatorios = ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_estimated_delivery_date']
    for campo in campos_obrigatorios:
        nulos = df[campo].isna().sum()
        if nulos > 0:
            avisos.append(f"{nulos} registros com {campo} nulo removidos")
            df = df[df[campo].notna()]
    
    # Converte timestamps
    campos_timestamp = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date']
    for campo in campos_timestamp:
        df[campo] = pd.to_datetime(df[campo], errors='coerce')
    
    # Converte data estimada
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'], errors='coerce')
    
    # Padroniza status
    df['order_status'] = df['order_status'].str.strip().str.lower()
    
    logger.info(f"Orders transformados: {len(df)} registros")
    
    return df, erros, avisos


def transform_order_items(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Transforma dados de order_items.
    
    Args:
        df: DataFrame raw de order_items
        
    Returns:
        Tupla (DataFrame transformado, erros, avisos)
    """
    erros = []
    avisos = []
    df = df.copy()
    
    # Valida campos obrigatórios
    campos_obrigatorios = ['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']
    for campo in campos_obrigatorios:
        nulos = df[campo].isna().sum()
        if nulos > 0:
            avisos.append(f"{nulos} registros com {campo} nulo removidos")
            df = df[df[campo].notna()]
    
    # Converte tipos
    df['order_item_id'] = df['order_item_id'].astype(int)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['freight_value'] = pd.to_numeric(df['freight_value'], errors='coerce')
    
    # Remove valores negativos
    df = df[df['price'] >= 0]
    df = df[df['freight_value'] >= 0]
    
    # Converte data limite
    df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
    
    logger.info(f"Order items transformados: {len(df)} registros")
    
    return df, erros, avisos


def transform_products(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Transforma dados de products.
    
    Args:
        df: DataFrame raw de products
        
    Returns:
        Tupla (DataFrame transformado, erros, avisos)
    """
    erros = []
    avisos = []
    df = df.copy()
    
    # Remove duplicatas por product_id
    duplicatas = df['product_id'].duplicated().sum()
    if duplicatas > 0:
        avisos.append(f"{duplicatas} registros duplicados removidos (product_id)")
        df = df.drop_duplicates(subset=['product_id'], keep='first')
    
    # Valida campo obrigatório
    nulos = df['product_id'].isna().sum()
    if nulos > 0:
        avisos.append(f"{nulos} registros com product_id nulo removidos")
        df = df[df['product_id'].notna()]
    
    # Converte tipos numéricos
    campos_numericos = [
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    for campo in campos_numericos:
        df[campo] = pd.to_numeric(df[campo], errors='coerce')
    
    # Padroniza categoria
    df['product_category_name'] = df['product_category_name'].str.strip().str.lower() if 'product_category_name' in df.columns else None
    
    logger.info(f"Products transformados: {len(df)} registros")
    
    return df, erros, avisos


def transform_order_payments(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """
    Transforma dados de order_payments.
    
    Args:
        df: DataFrame raw de order_payments
        
    Returns:
        Tupla (DataFrame transformado, erros, avisos)
    """
    erros = []
    avisos = []
    df = df.copy()
    
    # Valida campos obrigatórios
    campos_obrigatorios = ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']
    for campo in campos_obrigatorios:
        nulos = df[campo].isna().sum()
        if nulos > 0:
            avisos.append(f"{nulos} registros com {campo} nulo removidos")
            df = df[df[campo].notna()]
    
    # Converte tipos
    df['payment_sequential'] = df['payment_sequential'].astype(int)
    df['payment_installments'] = df['payment_installments'].astype(int)
    df['payment_value'] = pd.to_numeric(df['payment_value'], errors='coerce')
    
    # Remove valores negativos
    df = df[df['payment_value'] >= 0]
    df = df[df['payment_installments'] >= 0]
    
    # Padroniza tipo de pagamento
    df['payment_type'] = df['payment_type'].str.strip().str.lower()
    
    logger.info(f"Order payments transformados: {len(df)} registros")
    
    return df, erros, avisos


def transform_all(dataframes: Dict[str, pd.DataFrame]) -> Dict[str, Tuple[pd.DataFrame, List[str], List[str]]]:
    """
    Aplica transformação em todos os DataFrames do dataset Olist.
    
    Args:
        dataframes: Dicionário com nome da tabela e DataFrame raw
        
    Returns:
        Dicionário com nome da tabela e tupla (DataFrame transformado, erros, avisos)
    """
    logger.info("Iniciando transformação de todos os dados Olist")
    
    transformed = {}
    
    # Transforma cada tabela
    if 'customers' in dataframes:
        transformed['customers'] = transform_customers(dataframes['customers'])
    
    if 'orders' in dataframes:
        transformed['orders'] = transform_orders(dataframes['orders'])
    
    if 'order_items' in dataframes:
        transformed['order_items'] = transform_order_items(dataframes['order_items'])
    
    if 'products' in dataframes:
        transformed['products'] = transform_products(dataframes['products'])
    
    if 'order_payments' in dataframes:
        transformed['order_payments'] = transform_order_payments(dataframes['order_payments'])
    
    logger.info("Transformação concluída")
    
    return transformed
