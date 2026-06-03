"""
Rotas da API para operações com vendas.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from pathlib import Path

from database.connection import get_db
from backend.services.venda_service import VendaService
from backend.api.schemas.vendas import VendaResponse, CSVProcessResponse

router = APIRouter(prefix="/api/v1/vendas", tags=["vendas"])


@router.post("/upload", response_model=CSVProcessResponse)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Faz upload e processa um arquivo CSV de vendas.
    
    Args:
        file: Arquivo CSV enviado
        db: Sessão do banco de dados
        
    Returns:
        Resultado do processamento
    """
    # Valida se é um CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
    
    # Salva arquivo temporariamente
    temp_dir = Path("data/raw")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / file.filename
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Processa o CSV
        service = VendaService(db)
        resultado = service.processar_csv(str(temp_path))
        
        return resultado
        
    finally:
        # Remove arquivo temporário
        if temp_path.exists():
            temp_path.unlink()


@router.get("/", response_model=List[VendaResponse])
def listar_vendas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista vendas com paginação.
    
    Args:
        skip: Quantidade de registros para pular
        limit: Quantidade máxima de registros
        db: Sessão do banco de dados
        
    Returns:
        Lista de vendas
    """
    service = VendaService(db)
    vendas = service.listar_vendas(skip=skip, limit=limit)
    return vendas


@router.get("/{venda_id}", response_model=VendaResponse)
def obter_venda(
    venda_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca uma venda por ID.
    
    Args:
        venda_id: ID da venda
        db: Sessão do banco de dados
        
    Returns:
        Venda encontrada
    """
    service = VendaService(db)
    venda = service.obter_venda_por_id(venda_id)
    
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    return venda


@router.get("/contagem/total")
def contar_vendas(db: Session = Depends(get_db)):
    """
    Conta o total de vendas no banco.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Número total de vendas
    """
    service = VendaService(db)
    total = service.contar_vendas()
    return {"total": total}
