"""
Módulo de carga de dados do dataset Olist no banco de dados PostgreSQL.
"""
from typing import Dict, Tuple, List
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def load_to_database(
    transformed_data: Dict[str, Tuple],
    db: Session,
    batch_size: int = 1000
) -> Dict[str, Dict[str, int]]:
    """
    Carrega dados transformados no banco de dados.
    
    Args:
        transformed_data: Dicionário com nome da tabela e tupla (df, erros, avisos)
        db: Sessão do banco de dados
        batch_size: Tamanho do lote para inserção em batch
        
    Returns:
        Dicionário com estatísticas de carga por tabela
    """
    from backend.models import Customer, Product, Order, OrderItem, OrderPayment
    
    stats = {}
    
    # Carrega customers
    if 'customers' in transformed_data:
        df, erros, avisos = transformed_data['customers']
        stats['customers'] = _load_table(df, Customer, db, batch_size, 'customer_id')
    
    # Carrega products
    if 'products' in transformed_data:
        df, erros, avisos = transformed_data['products']
        stats['products'] = _load_table(df, Product, db, batch_size, 'product_id')
    
    # Carrega orders
    if 'orders' in transformed_data:
        df, erros, avisos = transformed_data['orders']
        stats['orders'] = _load_table(df, Order, db, batch_size, 'order_id')
    
    # Carrega order_items
    if 'order_items' in transformed_data:
        df, erros, avisos = transformed_data['order_items']
        stats['order_items'] = _load_table_composite(df, OrderItem, db, batch_size, ['order_id', 'order_item_id'])
    
    # Carrega order_payments
    if 'order_payments' in transformed_data:
        df, erros, avisos = transformed_data['order_payments']
        stats['order_payments'] = _load_table_composite(df, OrderPayment, db, batch_size, ['order_id', 'payment_sequential'])
    
    logger.info("Carga concluída")
    
    return stats


def _load_table(
    df,
    model_class,
    db: Session,
    batch_size: int,
    id_column: str
) -> Dict[str, int]:
    """
    Carrega dados em uma tabela com chave primária simples.
    
    Args:
        df: DataFrame com dados
        model_class: Classe do modelo SQLAlchemy
        db: Sessão do banco de dados
        batch_size: Tamanho do lote
        id_column: Nome da coluna ID
        
    Returns:
        Estatísticas da carga
    """
    stats = {
        'total_registros': len(df),
        'carregados': 0,
        'duplicatas': 0,
        'erros': 0
    }
    
    if len(df) == 0:
        logger.warning(f"DataFrame vazio para {model_class.__tablename__}")
        return stats
    
    # Converte DataFrame para lista de dicionários
    records = df.to_dict('records')
    
    # Processa em lotes
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        try:
            # Verifica duplicatas no banco
            ids = [r[id_column] for r in batch]
            existentes = set()
            
            for id_val in ids:
                existing = db.query(model_class).filter(getattr(model_class, id_column) == id_val).first()
                if existing:
                    existentes.add(id_val)
            
            # Filtra apenas registros não existentes
            novos_registros = [r for r in batch if r[id_column] not in existentes]
            
            if novos_registros:
                # Insere em batch
                db_objs = [model_class(**record) for record in novos_registros]
                db.add_all(db_objs)
                db.commit()
                stats['carregados'] += len(novos_registros)
                stats['duplicatas'] += len(existentes)
            else:
                stats['duplicatas'] += len(batch)
                
            logger.info(f"Batch {i//batch_size + 1} ({model_class.__tablename__}): {len(novos_registros)} novos registros")
            
        except Exception as e:
            logger.error(f"Erro ao carregar batch {i//batch_size + 1} ({model_class.__tablename__}): {str(e)}")
            db.rollback()
            stats['erros'] += len(batch)
    
    logger.info(f"Carga {model_class.__tablename__}: {stats['carregados']} registros carregados")
    
    return stats


def _load_table_composite(
    df,
    model_class,
    db: Session,
    batch_size: int,
    id_columns: List[str]
) -> Dict[str, int]:
    """
    Carrega dados em uma tabela com chave primária composta.
    
    Args:
        df: DataFrame com dados
        model_class: Classe do modelo SQLAlchemy
        db: Sessão do banco de dados
        batch_size: Tamanho do lote
        id_columns: Lista de nomes das colunas ID
        
    Returns:
        Estatísticas da carga
    """
    stats = {
        'total_registros': len(df),
        'carregados': 0,
        'duplicatas': 0,
        'erros': 0
    }
    
    if len(df) == 0:
        logger.warning(f"DataFrame vazio para {model_class.__tablename__}")
        return stats
    
    # Converte DataFrame para lista de dicionários
    records = df.to_dict('records')
    
    # Processa em lotes
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        try:
            # Verifica duplicatas no banco (para chave composta)
            existentes = 0
            novos_registros = []
            
            for record in batch:
                # Constrói filtro para chave composta
                filters = []
                for col in id_columns:
                    filters.append(getattr(model_class, col) == record[col])
                
                existing = db.query(model_class).filter(*filters).first()
                if existing:
                    existentes += 1
                else:
                    novos_registros.append(record)
            
            if novos_registros:
                # Insere em batch
                db_objs = [model_class(**record) for record in novos_registros]
                db.add_all(db_objs)
                db.commit()
                stats['carregados'] += len(novos_registros)
                stats['duplicatas'] += existentes
            else:
                stats['duplicatas'] += len(batch)
                
            logger.info(f"Batch {i//batch_size + 1} ({model_class.__tablename__}): {len(novos_registros)} novos registros")
            
        except Exception as e:
            logger.error(f"Erro ao carregar batch {i//batch_size + 1} ({model_class.__tablename__}): {str(e)}")
            db.rollback()
            stats['erros'] += len(batch)
    
    logger.info(f"Carga {model_class.__tablename__}: {stats['carregados']} registros carregados")
    
    return stats
