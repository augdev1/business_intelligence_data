# Sistema Inteligente de Análise Olist E-Commerce

Sistema profissional para análise de e-commerce brasileiro com dataset real Olist, processamento ETL, dashboards interativos modernos e consultas em linguagem natural via IA.

## Tecnologias

- **Backend:** Python 3.14.5, FastAPI
- **Banco de Dados:** PostgreSQL
- **Dataset:** Olist Brazilian E-Commerce (Kaggle)
- **Processamento:** Pandas, SQLAlchemy
- **IA:** LangChain (otimizado), Groq (llama-3.3-70b-versatile)
- **Frontend:** Streamlit
- **Visualização:** Plotly
- **Containerização:** Docker (opcional)

## Estrutura do Projeto

```
d:\dados_aug/
├── data/              # Arquivos de dados
│   └── raw/           # CSVs do dataset Olist
├── backend/           # API FastAPI e lógica de negócio
│   ├── models/        # Modelos SQLAlchemy Olist
│   ├── repositories/  # Repositories de dados
│   ├── services/      # Services de negócio
│   └── api/           # Rotas FastAPI
├── database/          # Configuração do banco
├── etl/               # Pipeline ETL Olist
├── ai/                # Assistente IA (LangChain + Groq)
├── frontend/          # Dashboard Streamlit (Design SaaS)
├── scripts/           # Scripts utilitários
├── tests/             # Testes
└── docs/              # Documentação
```

## Instalação Local

### Pré-requisitos

- Python 3.14.5
- PostgreSQL 14+
- Docker e Docker Compose (opcional)

### Passos

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente: `cp .env.example .env` e edite o arquivo
6. Inicie o PostgreSQL: `docker-compose up -d db` (ou use PostgreSQL local)
7. Carregue o dataset Olist: `python scripts/carregar_olist.py`
8. Inicie o backend: `uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000`
9. Inicie o frontend: `streamlit run frontend/app.py`

## Uso com Docker

```bash
docker-compose up -d
```

Acesse:
- Frontend: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Funcionalidades

- **Dataset Real:** Olist Brazilian E-Commerce (Kaggle)
- **ETL Pipeline:** Extração, transformação e carga dos 5 CSVs Olist
- **5 Tabelas Relacionadas:** customers, products, orders, order_items, order_payments
- **10 KPIs Analíticos:** Receita, pedidos, clientes, ticket médio, rankings, etc.
- **Dashboard SaaS Moderno:** 4 páginas com tema escuro elegante
- **IA com Groq:** Consultas em linguagem natural usando llama-3.3-70b-versatile

## KPIs Calculados

- Receita Total
- Número de Pedidos
- Clientes Únicos
- Ticket Médio
- Receita por Estado
- Receita por Mês
- Top 10 Produtos
- Top 10 Categorias
- Métodos de Pagamento
- Pedidos por Estado

## Dataset Olist

O sistema utiliza como fonte oficial de dados o dataset **Olist Brazilian E-Commerce** do Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

### Arquivos CSV Utilizados

- `olist_customers_dataset.csv` - Dados dos clientes (99,441 registros)
- `olist_orders_dataset.csv` - Pedidos realizados (99,441 registros)
- `olist_order_items_dataset.csv` - Itens de cada pedido (112,650 registros)
- `olist_products_dataset.csv` - Catálogo de produtos (32,951 registros)
- `olist_order_payments_dataset.csv` - Pagamentos dos pedidos (103,886 registros)

### Documentação Completa

Para análise detalhada do schema, chaves primárias/estrangeiras, diagrama ERD, KPIs definidos e arquitetura de dados, consulte:

**[docs/dataset_olist_analysis.md](docs/dataset_olist_analysis.md)**

Para auditoria completa do projeto e migração, consulte:

**[docs/auditoria_projeto.md](docs/auditoria_projeto.md)**

Para relatório final da migração, consulte:

**[docs/relatorio_final.md](docs/relatorio_final.md)**

## Como Carregar o Dataset Olist

Após configurar o PostgreSQL, execute o script de carga:

```bash
python scripts/carregar_olist.py
```

Este script irá:
1. Criar as 5 tabelas no PostgreSQL
2. Extrair os dados dos CSVs
3. Transformar e validar os dados
4. Carregar no banco em batch
5. Exibir estatísticas finais

## Desenvolvimento

### Executar Testes

```bash
pytest tests/
```

### Formatação de Código

```bash
black backend/ etl/ ai/ frontend/ tests/
```

## Licença

MIT
