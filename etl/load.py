"""
Módulo de carga de dados no banco de dados.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def load_to_database(
    df, 
    db: Session, 
    venda_repository,
    batch_size: int = 1000
) -> Dict[str, Any]:
    """
    Carrega dados do DataFrame para o banco de dados.
    
    Args:
        df: DataFrame com os dados transformados
        db: Sessão do banco de dados
        venda_repository: Instância de VendaRepository
        batch_size: Tamanho do lote para inserção em batch
        
    Returns:
        Dicionário com estatísticas da carga
    """
    stats = {
        'total_registros': len(df),
        'carregados': 0,
        'duplicatas': 0,
        'erros': 0
    }
    
    if len(df) == 0:
        logger.warning("DataFrame vazio, nada para carregar")
        return stats
    
    # Converte DataFrame para lista de dicionários
    records = df.to_dict('records')
    
    # Processa em lotes
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        try:
            # Verifica duplicatas no banco
            ids_venda = [r['id_venda'] for r in batch]
            existentes = set()
            for id_venda in ids_venda:
                if venda_repository.get_by_id_venda(id_venda):
                    existentes.add(id_venda)
            
            # Filtra apenas registros não existentes
            novos_registros = [r for r in batch if r['id_venda'] not in existentes]
            
            if novos_registros:
                # Converte datetime para date
                for record in novos_registros:
                    if hasattr(record['data_venda'], 'date'):
                        record['data_venda'] = record['data_venda'].date()
                
                # Insere em batch
                venda_repository.create_many(novos_registros)
                stats['carregados'] += len(novos_registros)
                stats['duplicatas'] += len(existentes)
            else:
                stats['duplicatas'] += len(batch)
                
            logger.info(f"Batch {i//batch_size + 1}: {len(novos_registros)} novos registros")
            
        except Exception as e:
            logger.error(f"Erro ao carregar batch {i//batch_size + 1}: {str(e)}")
            stats['erros'] += len(batch)
    
    logger.info(f"Carga concluída: {stats['carregados']} registros carregados")
    
    return stats


def load_single_record(record: Dict[str, Any], db: Session, venda_repository) -> bool:
    """
    Carrega um único registro no banco de dados.
    
    Args:
        record: Dicionário com os dados do registro
        db: Sessão do banco de dados
        venda_repository: Instância de VendaRepository
        
    Returns:
        True se carregado com sucesso, False caso contrário
    """
    try:
        # Verifica se já existe
        if venda_repository.get_by_id_venda(record['id_venda']):
            logger.warning(f"Registro duplicado: {record['id_venda']}")
            return False
        
        # Converte datetime para date se necessário
        if hasattr(record['data_venda'], 'date'):
            record['data_venda'] = record['data_venda'].date()
        
        # Cria registro
        venda_repository.create(record)
        return True
        
    except Exception as e:
        logger.error(f"Erro ao carregar registro {record.get('id_venda', 'unknown')}: {str(e)}")
        return False
