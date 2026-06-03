"""
Rotas da API para consultas via IA.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.ia_service import IAService
from backend.api.schemas.vendas import IAPerguntaRequest, IAPerguntaResponse

router = APIRouter(prefix="/api/v1/ia", tags=["ia"])


@router.post("/perguntar", response_model=IAPerguntaResponse)
def perguntar(
    request: IAPerguntaRequest,
    db: Session = Depends(get_db)
):
    """
    Processa uma pergunta em linguagem natural.
    
    Args:
        request: Pergunta do usuário
        db: Sessão do banco de dados
        
    Returns:
        Resposta da IA com SQL gerado e dados
    """
    service = IAService(db)
    resultado = service.perguntar(request.pergunta)
    return resultado
