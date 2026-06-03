# Arquitetura do Sistema

## Visão Geral

O Sistema de Análise de Vendas segue uma arquitetura em camadas (layered architecture) com separação clara de responsabilidades.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                     │
│                  Dashboard Interativo                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
┌──────────────────────────▼──────────────────────────────────┐
│                   API Layer (FastAPI)                        │
│              Endpoints e Validação de Requisições            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Business Logic Layer (Services)                 │
│    Serviços de Domínio e Cálculo de Indicadores              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Data Access Layer (Repositories)                │
│           Abstração de Acesso ao Banco de Dados              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              ORM Layer (SQLAlchemy Models)                   │
│               Mapeamento Objeto-Relacional                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  PostgreSQL Database                         │
│              Armazenamento Persistente de Dados              │
└─────────────────────────────────────────────────────────────┘
```

## Camadas do Sistema

### 1. Frontend (Streamlit)

**Responsabilidade:** Interface visual para usuários.

**Arquivos:**
- `frontend/app.py` - Aplicação principal do dashboard

**Funcionalidades:**
- Dashboard com KPIs e gráficos interativos
- Upload de arquivos CSV
- Chat interface para consultas em linguagem natural

### 2. API Layer (FastAPI)

**Responsabilidade:** Expor endpoints REST.

**Arquivos:**
- `backend/api/main.py` - Aplicação FastAPI
- `backend/api/routes/vendas.py` - Rotas de vendas
- `backend/api/routes/indicadores.py` - Rotas de indicadores
- `backend/api/routes/ia.py` - Rotas de IA
- `backend/api/schemas/vendas.py` - Schemas Pydantic

**Endpoints:**
- `POST /api/v1/vendas/upload` - Upload de CSV
- `GET /api/v1/vendas/` - Listar vendas
- `GET /api/v1/indicadores/` - Todos os indicadores
- `POST /api/v1/ia/perguntar` - Consulta via IA

### 3. Business Logic Layer (Services)

**Responsabilidade:** Implementar regras de negócio.

**Arquivos:**
- `backend/services/venda_service.py` - Serviço de vendas
- `backend/services/indicador_service.py` - Serviço de indicadores
- `backend/services/ia_service.py` - Serviço de IA

### 4. Data Access Layer (Repositories)

**Responsabilidade:** Abstrair acesso ao banco de dados.

**Arquivos:**
- `backend/repositories/base.py` - Repository base
- `backend/repositories/venda_repository.py` - Repository de vendas

### 5. ORM Layer (SQLAlchemy)

**Responsabilidade:** Mapear tabelas para objetos Python.

**Arquivos:**
- `database/connection.py` - Configuração de conexão
- `backend/models/venda.py` - Modelo Venda

### 6. ETL Pipeline

**Responsabilidade:** Processamento batch de CSV.

**Arquivos:**
- `etl/extract.py` - Extração de dados
- `etl/transform.py` - Transformação e validação
- `etl/load.py` - Carga no banco

### 7. AI Layer (LangChain)

**Responsabilidade:** Consultas em linguagem natural.

**Arquivos:**
- `ai/sql_chain.py` - Chain SQL do LangChain (otimizado com LCEL)
- `ai/prompts.py` - Templates de prompt

**Otimizações:**
- Uso de LCEL (LangChain Expression Language) para melhor performance
- Cache em memória para evitar chamadas repetidas ao LLM
- Modelos otimizados: gpt-4o-mini (OpenAI) e llama-3.1-70b-versatile (Groq)
- Prompts concisos para reduzir tokens
- Timeout configurado para evitar travamentos
- max_tokens limitado para respostas mais rápidas

## Modelo de Dados

### Fonte de Dados Oficial

**Dataset:** Olist Brazilian E-Commerce  
**URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
**Licença:** CC-BY-NC-SA-4.0

Para análise completa do schema, PKs, FKs, ERD, KPIs e arquitetura de dados, consulte:  
**[docs/dataset_olist_analysis.md](dataset_olist_analysis.md)**

### Schema Principal (Olist)

O sistema utiliza o dataset Olist com as seguintes tabelas principais:

- **customers** - Dados dos clientes
- **products** - Catálogo de produtos
- **orders** - Pedidos realizados
- **order_items** - Itens de cada pedido
- **order_payments** - Pagamentos dos pedidos

### Schema Legado (Vendas Simples)

```sql
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    id_venda VARCHAR(50) UNIQUE NOT NULL,
    data_venda DATE NOT NULL,
    produto VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    valor_unitario DECIMAL(10, 2) NOT NULL CHECK (valor_unitario >= 0),
    faturamento DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Nota:** A tabela `vendas` é mantida para compatibilidade com o sistema original. O novo sistema utiliza o schema Olist para análise de e-commerce.

## Fluxo de Dados

### Importação de CSV

```
CSV → Extract → Transform → Load → PostgreSQL
```

### Consulta de Indicadores

```
Frontend → API → Service → Repository → PostgreSQL → Repository → Service → API → Frontend
```

### Consulta via IA

```
Usuário → Frontend → API → IA Service → LangChain → LLM → SQL → PostgreSQL → Resultados → LLM → Resposta → Frontend
```

## Padrões de Projeto

- **Repository Pattern:** Abstração de acesso a dados
- **Dependency Injection:** Injeção de dependências via FastAPI
- **Service Layer:** Separação de lógica de negócio
- **DTO Pattern:** Schemas Pydantic para transferência de dados
- **Factory Pattern:** Criação de sessões de banco
