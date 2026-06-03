"""
Schemas Pydantic para validação de dados de vendas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from decimal import Decimal


class VendaBase(BaseModel):
    """Schema base para venda."""
    id_venda: str = Field(..., description="Identificador único da venda")
    data_venda: date = Field(..., description="Data da venda")
    produto: str = Field(..., description="Nome do produto")
    categoria: str = Field(..., description="Categoria do produto")
    cidade: str = Field(..., description="Cidade da venda")
    quantidade: int = Field(..., gt=0, description="Quantidade vendida")
    valor_unitario: Decimal = Field(..., ge=0, description="Valor unitário")


class VendaCreate(VendaBase):
    """Schema para criação de venda."""
    pass


class VendaResponse(VendaBase):
    """Schema para resposta de venda."""
    id: int
    faturamento: Decimal
    
    class Config:
        from_attributes = True


class IndicadoresResponse(BaseModel):
    """Schema para resposta de indicadores."""
    faturamento_total: Decimal
    quantidade_total: int
    ticket_medio: Decimal
    produto_mais_vendido: Optional[dict]
    categoria_mais_vendida: Optional[dict]
    cidade_maior_faturamento: Optional[dict]
    evolucao_mensal: List[dict]
    ranking_produtos: List[dict]
    ranking_cidades: List[dict]
    total_vendas: int


class CSVProcessResponse(BaseModel):
    """Schema para resposta de processamento de CSV."""
    sucesso: bool
    mensagem: str
    estatisticas: Optional[dict]
    erros: List[str]
    avisos: List[str]


class IAPerguntaRequest(BaseModel):
    """Schema para requisição de pergunta à IA."""
    pergunta: str = Field(..., description="Pergunta em linguagem natural")


class IAPerguntaResponse(BaseModel):
    """Schema para resposta da IA."""
    sucesso: bool
    pergunta: str
    resposta: str
    sql: Optional[str]
    dados: Optional[list]
