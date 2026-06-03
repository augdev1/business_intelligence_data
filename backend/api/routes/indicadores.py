"""
Rotas da API para consultas de indicadores.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from database.connection import get_db
from backend.services.indicador_service import IndicadorService
from backend.api.schemas.vendas import IndicadoresResponse

router = APIRouter(prefix="/api/v1/indicadores", tags=["indicadores"])


@router.get("/", response_model=IndicadoresResponse)
def obter_todos_indicadores(db: Session = Depends(get_db)):
    """
    Retorna todos os indicadores de negócio.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Todos os indicadores calculados
    """
    service = IndicadorService(db)
    indicadores = service.calcular_todos_indicadores()
    return indicadores


@router.get("/faturamento-total")
def obter_faturamento_total(db: Session = Depends(get_db)):
    """
    Retorna o faturamento total.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Faturamento total
    """
    service = IndicadorService(db)
    return {"faturamento_total": service.get_faturamento_total()}


@router.get("/quantidade-total")
def obter_quantidade_total(db: Session = Depends(get_db)):
    """
    Retorna a quantidade total vendida.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Quantidade total
    """
    service = IndicadorService(db)
    return {"quantidade_total": service.get_quantidade_total()}


@router.get("/ticket-medio")
def obter_ticket_medio(db: Session = Depends(get_db)):
    """
    Retorna o ticket médio.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Ticket médio
    """
    service = IndicadorService(db)
    return {"ticket_medio": service.get_ticket_medio()}


@router.get("/evolucao-mensal")
def obter_evolucao_mensal(db: Session = Depends(get_db)):
    """
    Retorna a evolução mensal das vendas.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Lista de dados mensais
    """
    service = IndicadorService(db)
    return {"evolucao_mensal": service.get_evolucao_mensal()}


@router.get("/ranking-produtos")
def obter_ranking_produtos(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna o ranking de produtos.
    
    Args:
        limit: Quantidade máxima de produtos
        db: Sessão do banco de dados
        
    Returns:
        Lista de produtos no ranking
    """
    service = IndicadorService(db)
    return {"ranking_produtos": service.get_ranking_produtos(limit=limit)}


@router.get("/ranking-cidades")
def obter_ranking_cidades(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna o ranking de cidades.
    
    Args:
        limit: Quantidade máxima de cidades
        db: Sessão do banco de dados
        
    Returns:
        Lista de cidades no ranking
    """
    service = IndicadorService(db)
    return {"ranking_cidades": service.get_ranking_cidades(limit=limit)}


@router.get("/periodo")
def obter_vendas_por_periodo(
    data_inicio: date,
    data_fim: date,
    db: Session = Depends(get_db)
):
    """
    Retorna vendas em um período específico.
    
    Args:
        data_inicio: Data inicial
        data_fim: Data final
        db: Sessão do banco de dados
        
    Returns:
        Lista de vendas no período
    """
    service = IndicadorService(db)
    vendas = service.get_vendas_por_periodo(data_inicio, data_fim)
    return {"vendas": vendas}
