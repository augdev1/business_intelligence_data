"""
Aplicação principal FastAPI - Dataset Olist Brazilian E-Commerce.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import kpi, ia
from database.connection import init_db

# Cria aplicação FastAPI
app = FastAPI(
    title="Sistema de Análise Olist E-Commerce",
    description="API para análise de e-commerce com dataset Olist e capacidades de IA",
    version="2.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas
app.include_router(kpi.router)
app.include_router(ia.router)


@app.on_event("startup")
async def startup_event():
    """
    Evento de startup da aplicação.
    Inicializa o banco de dados.
    """
    init_db()


@app.get("/")
def root():
    """
    Rota raiz.
    Retorna informações básicas da API.
    """
    return {
        "message": "Sistema de Análise Olist E-Commerce",
        "version": "2.0.0",
        "dataset": "Olist Brazilian E-Commerce",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Rota de health check.
    """
    return {"status": "healthy"}
