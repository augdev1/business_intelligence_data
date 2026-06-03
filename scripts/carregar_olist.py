"""
Script para carregar o dataset Olist no banco de dados.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.connection import SessionLocal, init_db
from etl.extract_olist import extract_olist_csvs
from etl.transform_olist import transform_all
from etl.load_olist import load_to_database
import logging

# Configura logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Função principal para carregar o dataset Olist."""
    logger.info("Iniciando carga do dataset Olist...")
    
    # Inicializa o banco de dados
    logger.info("Criando tabelas no banco de dados...")
    init_db()
    
    # Cria sessão do banco
    db = SessionLocal()
    
    try:
        # Extract
        logger.info("=== EXTRACT ===")
        dataframes = extract_olist_csvs(data_dir="data/raw")
        
        # Transform
        logger.info("=== TRANSFORM ===")
        transformed = transform_all(dataframes)
        
        # Load
        logger.info("=== LOAD ===")
        stats = load_to_database(transformed, db, batch_size=1000)
        
        # Exibe estatísticas finais
        logger.info("=== ESTATÍSTICAS FINAIS ===")
        total_carregados = sum(s['carregados'] for s in stats.values())
        total_duplicatas = sum(s['duplicatas'] for s in stats.values())
        total_erros = sum(s['erros'] for s in stats.values())
        
        logger.info(f"Total de registros carregados: {total_carregados}")
        logger.info(f"Total de duplicatas ignoradas: {total_duplicatas}")
        logger.info(f"Total de erros: {total_erros}")
        
        for tabela, stat in stats.items():
            logger.info(f"{tabela}: {stat['carregados']} carregados, {stat['duplicatas']} duplicatas, {stat['erros']} erros")
        
        logger.info("Carga concluída com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante a carga: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
