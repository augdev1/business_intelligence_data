# Guia de Instalação

## Pré-requisitos

- Python 3.14.5
- PostgreSQL 14 ou superior
- pip (gerenciador de pacotes Python)
- Docker e Docker Compose (opcional, para execução com containers)

## Instalação Local

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd projeto_analise_vendas
```

### 2. Crie Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ative o Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale Dependências

```bash
pip install -r requirements.txt
```

### 5. Configure Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure as variáveis:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/vendas_db

# AI Provider (openai ou groq)
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8501
API_URL=http://localhost:8000
```

### 6. Configure o PostgreSQL

#### Opção A: PostgreSQL Local

Crie o banco de dados:

```bash
createdb vendas_db
```

Ou usando psql:

```sql
CREATE DATABASE vendas_db;
```

#### Opção B: PostgreSQL com Docker

```bash
docker run --name vendas_db \
  -e POSTGRES_USER=vendas_user \
  -e POSTGRES_PASSWORD=vendas_password \
  -e POSTGRES_DB=vendas_db \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### 7. Inicialize o Banco de Dados

O banco será criado automaticamente ao iniciar a API. Para criar manualmente:

```bash
python -c "from database.connection import init_db; init_db()"
```

### 8. Inicie o Backend

```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: http://localhost:8000

### 9. Inicie o Frontend

Em um novo terminal:

```bash
streamlit run frontend/app.py
```

O dashboard estará disponível em: http://localhost:8501

## Instalação com Docker

### 1. Configure Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário.

### 2. Inicie Todos os Serviços

```bash
cd docker
docker-compose up -d
```

### 3. Verifique os Serviços

```bash
docker-compose ps
```

### 4. Acesse as Aplicações

- Frontend: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 5. Pare os Serviços

```bash
docker-compose down
```

Para remover volumes (dados do banco):

```bash
docker-compose down -v
```

## Verificação da Instalação

### Verificar API

```bash
curl http://localhost:8000/
```

Resposta esperada:
```json
{
  "message": "Sistema de Análise de Vendas",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### Verificar Health Check

```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{
  "status": "healthy"
}
```

### Executar Testes

```bash
pytest tests/
```

## Solução de Problemas

### Erro: "psycopg2.OperationalError: could not connect to server"

**Causa:** PostgreSQL não está rodando ou configuração incorreta.

**Solução:**
1. Verifique se PostgreSQL está rodando
2. Verifique a string de conexão no `.env`
3. Verifique se o banco de dados existe

### Erro: "OPENAI_API_KEY não configurada"

**Causa:** Chave da API não configurada.

**Solução:**
1. Configure `OPENAI_API_KEY` no `.env`
2. Ou use `AI_PROVIDER=groq` com `GROQ_API_KEY`

### Erro: "ModuleNotFoundError"

**Causa:** Dependências não instaladas.

**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: Porta já em uso

**Causa:** Porta 8000 ou 8501 já está em uso.

**Solução:**
1. Mude as portas no `.env`
2. Ou mate o processo usando a porta:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

## Próximos Passos

Após a instalação:

1. Acesse o dashboard em http://localhost:8501
2. Faça upload de um arquivo CSV na aba "Upload CSV"
3. Visualize os indicadores na aba "Dashboard"
4. Faça perguntas na aba "Assistente IA"

## Estrutura de Arquivo CSV de Exemplo

```csv
id_venda,data_venda,produto,categoria,cidade,quantidade,valor_unitario
V001,2024-01-01,Produto A,Categoria A,São Paulo,10,100.00
V002,2024-01-02,Produto B,Categoria B,Rio de Janeiro,20,200.00
V003,2024-01-03,Produto C,Categoria A,Belo Horizonte,15,150.00
```
