"""
Serviço de negócio para operações com vendas.
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
import logging

from backend.repositories.venda_repository import VendaRepository
from etl.extract import extract_csv
from etl.transform import transform
from etl.load import load_to_database

logger = logging.getLogger(__name__)


class VendaService:
    """
    Serviço para operações de negócio relacionadas a vendas.
    
    Coordena o pipeline ETL e operações de CRUD.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de vendas.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = VendaRepository(db)
    
    def processar_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Processa um arquivo CSV completo (ETL).
        
        Args:
            file_path: Caminho do arquivo CSV
            
        Returns:
            Dicionário com resultado do processamento
        """
        try:
            # Extract
            logger.info(f"Iniciando extração do arquivo: {file_path}")
            df = extract_csv(file_path)
            
            # Transform
            logger.info("Iniciando transformação dos dados")
            df_transformado, erros, avisos = transform(df)
            
            if len(df_transformado) == 0 and erros:
                return {
                    'sucesso': False,
                    'mensagem': 'Erro na transformação dos dados',
                    'erros': erros,
                    'avisos': avisos
                }
            
            # Load
            logger.info("Iniciando carga no banco de dados")
            stats = load_to_database(df_transformado, self.db, self.repository)
            
            return {
                'sucesso': True,
                'mensagem': 'CSV processado com sucesso',
                'estatisticas': stats,
                'erros': erros,
                'avisos': avisos
            }
            
        except FileNotFoundError as e:
            logger.error(f"Arquivo não encontrado: {str(e)}")
            return {
                'sucesso': False,
                'mensagem': f'Arquivo não encontrado: {str(e)}',
                'erros': [str(e)],
                'avisos': []
            }
        except Exception as e:
            logger.error(f"Erro ao processar CSV: {str(e)}")
            return {
                'sucesso': False,
                'mensagem': f'Erro ao processar CSV: {str(e)}',
                'erros': [str(e)],
                'avisos': []
            }
    
    def listar_vendas(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """
        Lista vendas com paginação.
        
        Args:
            skip: Quantidade de registros para pular
            limit: Quantidade máxima de registros
            
        Returns:
            Lista de vendas
        """
        return self.repository.get_all(skip=skip, limit=limit)
    
    def obter_venda_por_id(self, venda_id: int) -> Any:
        """
        Busca uma venda por ID.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            Instância de Venda ou None
        """
        return self.repository.get(venda_id)
    
    def contar_vendas(self) -> int:
        """
        Conta o total de vendas no banco.
        
        Returns:
            Número total de vendas
        """
        return self.repository.count()
