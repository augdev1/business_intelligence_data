"""
Rotas da API para consultas de KPIs do dataset Olist.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.kpi_service import KPIService

router = APIRouter(prefix="/api/v1/kpi", tags=["kpi"])


@router.get("/")
def obter_todos_kpis(db: Session = Depends(get_db)):
    """
    Retorna todos os KPIs de negócio do dataset Olist.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Todos os KPIs calculados
    """
    service = KPIService(db)
    kpis = service.calcular_todos_kpis()
    return kpis


@router.get("/receita-total")
def obter_receita_total(db: Session = Depends(get_db)):
    """
    Retorna a receita total.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Receita total
    """
    service = KPIService(db)
    return {"receita_total": service.get_receita_total()}


@router.get("/numero-pedidos")
def obter_numero_pedidos(db: Session = Depends(get_db)):
    """
    Retorna o número de pedidos.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Número de pedidos
    """
    service = KPIService(db)
    return {"numero_pedidos": service.get_numero_pedidos()}


@router.get("/clientes-unicos")
def obter_clientes_unicos(db: Session = Depends(get_db)):
    """
    Retorna o número de clientes únicos.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Número de clientes únicos
    """
    service = KPIService(db)
    return {"clientes_unicos": service.get_clientes_unicos()}


@router.get("/ticket-medio")
def obter_ticket_medio(db: Session = Depends(get_db)):
    """
    Retorna o ticket médio.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Ticket médio
    """
    service = KPIService(db)
    return {"ticket_medio": service.get_ticket_medio()}


@router.get("/receita-por-estado")
def obter_receita_por_estado(db: Session = Depends(get_db)):
    """
    Retorna a receita por estado.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Receita por estado
    """
    service = KPIService(db)
    return {"receita_por_estado": service.get_receita_por_estado()}


@router.get("/receita-por-mes")
def obter_receita_por_mes(db: Session = Depends(get_db)):
    """
    Retorna a receita por mês.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Receita por mês
    """
    service = KPIService(db)
    return {"receita_por_mes": service.get_receita_por_mes()}


@router.get("/top-produtos")
def obter_top_produtos(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna os top produtos.
    
    Args:
        limit: Quantidade máxima de produtos
        db: Sessão do banco de dados
        
    Returns:
        Lista de produtos no ranking
    """
    service = KPIService(db)
    return {"top_produtos": service.get_top_produtos(limit=limit)}


@router.get("/top-categorias")
def obter_top_categorias(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna as top categorias.
    
    Args:
        limit: Quantidade máxima de categorias
        db: Sessão do banco de dados
        
    Returns:
        Lista de categorias no ranking
    """
    service = KPIService(db)
    return {"top_categorias": service.get_top_categorias(limit=limit)}


@router.get("/metodos-pagamento")
def obter_metodos_pagamento(db: Session = Depends(get_db)):
    """
    Retorna os métodos de pagamento.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Métodos de pagamento
    """
    service = KPIService(db)
    return {"metodos_pagamento": service.get_metodos_pagamento()}


@router.get("/pedidos-por-estado")
def obter_pedidos_por_estado(db: Session = Depends(get_db)):
    """
    Retorna os pedidos por estado.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Pedidos por estado
    """
    service = KPIService(db)
    return {"pedidos_por_estado": service.get_pedidos_por_estado()}
