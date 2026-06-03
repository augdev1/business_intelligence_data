"""
Serviço de integração com IA para consultas em linguagem natural.
Dataset Olist Brazilian E-Commerce.
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
import os

from backend.repositories.kpi_repository import KPIRepository
from ai.sql_chain import SQLChain

logger = logging.getLogger(__name__)


class IAService:
    """
    Serviço para integração com IA.
    
    Implementa a funcionalidade de consultas em linguagem natural
    usando LangChain e LLM (Groq - llama-3.3-70b-versatile).
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de IA.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = KPIRepository(db)
        self.ai_provider = os.getenv('AI_PROVIDER', 'groq')  # Default para Groq
        
        try:
            self.sql_chain = SQLChain(ai_provider=self.ai_provider)
            logger.info(f"IA configurada com provider: {self.ai_provider}")
        except Exception as e:
            logger.error(f"Erro ao configurar IA: {str(e)}")
            self.sql_chain = None
    
    def perguntar(self, pergunta: str) -> Dict[str, Any]:
        """
        Processa uma pergunta em linguagem natural.
        
        Args:
            pergunta: Pergunta do usuário
            
        Returns:
            Dicionário com a resposta e SQL gerado
        """
        try:
            logger.info(f"Processando pergunta: {pergunta}")
            
            if not self.sql_chain:
                return {
                    'sucesso': False,
                    'pergunta': pergunta,
                    'resposta': 'IA não configurada. Verifique as variáveis de ambiente.',
                    'sql': None,
                    'dados': None
                }
            
            # Gera SQL
            sql = self.sql_chain.generate_sql(pergunta)
            
            # Executa SQL no banco
            try:
                resultados = self.repository.execute_raw_query(sql)
                logger.info(f"Query executada com sucesso: {len(resultados)} resultados")
            except Exception as e:
                logger.error(f"Erro ao executar SQL: {str(e)}")
                return {
                    'sucesso': False,
                    'pergunta': pergunta,
                    'resposta': f'Erro ao executar query: {str(e)}',
                    'sql': sql,
                    'dados': None
                }
            
            # Formata resposta em linguagem natural
            resposta = self.sql_chain.format_response(pergunta, sql, resultados)
            
            return {
                'sucesso': True,
                'pergunta': pergunta,
                'resposta': resposta,
                'sql': sql,
                'dados': resultados
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar pergunta: {str(e)}")
            return {
                'sucesso': False,
                'pergunta': pergunta,
                'resposta': f'Erro ao processar pergunta: {str(e)}',
                'sql': None,
                'dados': None
            }
