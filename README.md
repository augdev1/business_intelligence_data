# Sistema Inteligente de Análise Olist E-Commerce

Sistema profissional de Business Intelligence e Análise de Dados implementando pipeline ETL completo, dashboard interativo moderno e assistente de IA para consultas em linguagem natural sobre dataset real de e-commerce brasileiro.

## 🎯 Visão Geral

Este projeto demonstra competências avançadas em engenharia de dados, incluindo:

- **Pipeline ETL profissional** para processamento de dataset real (Olist Brazilian E-Commerce - 100k+ registros)
- **Arquitetura em camadas** seguindo melhores práticas (Repository Pattern, Service Layer, DTO Pattern)
- **Dashboard interativo** com design SaaS moderno e 4 páginas analíticas
- **Assistente de IA** usando LangChain + Groq (llama-3.3-70b-versatile) para consultas em linguagem natural
- **API REST** com FastAPI para exposição de KPIs e endpoints analíticos
- **Banco de dados relacional** PostgreSQL com schema normalizado e índices otimizados

## 🛠️ Stack Tecnológico

### Backend & API
- **Python 3.12+** - Linguagem principal
- **FastAPI 0.115.0** - Framework API REST de alta performance
- **SQLAlchemy 2.0.35** - ORM para mapeamento objeto-relacional
- **Pydantic 2.9.2** - Validação de dados e schemas
- **Uvicorn** - Servidor ASGI

### Banco de Dados
- **PostgreSQL 14+** - Banco de dados relacional
- **psycopg2-binary** - Driver PostgreSQL para Python

### Processamento de Dados
- **Pandas 2.2.3** - Manipulação e análise de dados
- **NumPy 2.1.3** - Computação numérica

### Inteligência Artificial
- **LangChain 0.3.7** - Framework para desenvolvimento com LLMs
- **LangChain Groq 0.2.1** - Integração com Groq API
- **llama-3.3-70b-versatile** - Modelo LLM de alta performance
- **LCEL (LangChain Expression Language)** - Chains otimizadas para performance

### Frontend & Visualização
- **React 18** - Framework de UI
- **Vite** - Build tool e dev server (porta 3000)
- **TypeScript** - Tipagem estática
- **Tailwind CSS v4** - Estilização utility-first
- **Recharts** - Gráficos interativos e responsivos
- **Framer Motion** - Animações fluidas
- **Lucide React** - Ícones
- **React Router v6** - Roteamento SPA

### Testes & Qualidade
- **pytest 8.3.3** - Framework de testes
- **pytest-asyncio** - Suporte a testes assíncronos
- **Black** - Formatação de código

### DevOps
- **PowerShell Scripts** - Automação de setup

## 📁 Estrutura do Projeto

```
d:\dados_aug/
├── data/
│   ├── raw/                    # CSVs originais do dataset Olist (100k+ registros)
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   └── olist_order_payments_dataset.csv
│   └── processed/              # Dados processados
├── backend/
│   ├── api/                    # API FastAPI
│   │   ├── main.py             # Aplicação principal
│   │   ├── routes/             # Endpoints REST (kpi, ia)
│   │   └── schemas/            # Schemas Pydantic
│   ├── models/                 # Modelos SQLAlchemy (5 tabelas Olist)
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── order_payment.py
│   ├── repositories/           # Repository Pattern (acesso a dados)
│   │   ├── base.py
│   │   ├── customer_repository.py
│   │   └── kpi_repository.py
│   └── services/               # Service Layer (lógica de negócio)
│       ├── indicador_service.py
│       └── ia_service.py
├── database/
│   └── connection.py           # Configuração PostgreSQL
├── etl/                        # Pipeline ETL profissional
│   ├── extract_olist.py        # Extração dos CSVs
│   ├── transform_olist.py      # Transformação e validação
│   └── load_olist.py           # Carga em batch no PostgreSQL
├── ai/                         # Assistente IA com LangChain
│   ├── sql_chain.py            # Chain SQL otimizado com LCEL
│   └── prompts.py              # Templates de prompt
├── frontend/
│   └── app.py                  # Dashboard Streamlit (legado)
├── frontend-react/             # Dashboard React + Vite + TypeScript
│   ├── src/
│   │   ├── pages/              # Visão Executiva, Produtos, Clientes, Assistente IA
│   │   ├── components/         # Sidebar, ChartCard, GradientSelector
│   │   ├── context/            # ThemeContext (dark/light)
│   │   ├── hooks/              # useKPIs
│   │   └── lib/                # api.ts, utils.ts
│   ├── vite.config.ts
│   └── package.json
├── scripts/
│   ├── carregar_olist.py       # Script de carga original
│   └── carregar_rapido.py      # Carga rápida via bulk insert (ON CONFLICT DO NOTHING)
├── tests/                      # Testes unitários e integração
├── docs/                       # Documentação técnica detalhada
│   ├── arquitetura.md          # Diagrama de arquitetura
│   ├── dataset_olist_analysis.md  # Análise completa do schema
│   ├── api_documentation.md    # Documentação da API
│   └── auditoria_projeto.md    # Auditoria técnica
├── docker/                     # Configuração Docker (opcional)
├── requirements.txt            # Dependências Python
├── pyproject.toml              # Configuração do projeto
└── start_dashboard.ps1         # Script de automação (Windows)
```

## 🏗️ Arquitetura do Sistema

O sistema implementa uma **arquitetura em camadas (layered architecture)** com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│              Frontend (React + Vite + TypeScript)           │
│         Dashboard SPA - 4 Páginas · localhost:3000          │
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
│              5 Tabelas Relacionais (Schema Olist)            │
└─────────────────────────────────────────────────────────────┘
```

### Padrões de Projeto Implementados

- **Repository Pattern:** Abstração de acesso a dados
- **Service Layer:** Separação de lógica de negócio
- **DTO Pattern:** Schemas Pydantic para transferência de dados
- **Dependency Injection:** Injeção de dependências via FastAPI

## 📊 Dataset Olist Brazilian E-Commerce

O sistema utiliza como fonte oficial de dados o dataset **Olist Brazilian E-Commerce** do Kaggle:

**Fonte:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
**Licença:** CC-BY-NC-SA-4.0  
**Volume de Dados:** 100k+ registros distribuídos em 5 tabelas relacionais

### Tabelas do Dataset

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `customers` | 99,441 | Dados demográficos dos clientes |
| `orders` | 99,441 | Pedidos realizados com status e timestamps |
| `order_items` | 112,650 | Itens de cada pedido (preço, frete) |
| `products` | 32,951 | Catálogo de produtos com categorias |
| `order_payments` | 103,886 | Pagamentos (tipo, parcelas, valor) |

### Relacionamentos

- **customers ↔ orders:** 1:N (um cliente, múltiplos pedidos)
- **orders ↔ order_items:** 1:N (um pedido, múltiplos itens)
- **orders ↔ order_payments:** 1:N (um pedido, múltiplos pagamentos)
- **products ↔ order_items:** 1:N (um produto, múltiplos itens)

### Schema do Banco PostgreSQL

O banco de dados implementa o schema normalizado do Olist com:

- **Chaves primárias (PK)** em todas as tabelas
- **Chaves estrangeiras (FK)** para integridade referencial
- **Índices** nas colunas frequentemente usadas em joins e filtros
- **Constraints** para validação de dados

Para análise completa do schema, ERD e KPIs definidos, consulte: **[docs/dataset_olist_analysis.md](docs/dataset_olist_analysis.md)**

## 🔄 Pipeline ETL

O sistema implementa um pipeline ETL profissional em 3 fases:

### Extract (Extração)
- Leitura dos 5 arquivos CSV principais do dataset Olist
- Validação de schema (colunas e tipos de dados)
- Detecção de arquivos ausentes ou corrompidos
- Logging detalhado de cada etapa

### Transform (Transformação)
- Conversão de tipos (strings para datas, números, timestamps)
- Tratamento de valores nulos e outliers
- Normalização de categorias de produtos
- Validação de integridade referencial
- Cálculo de campos derivados (ex: total_order_value)

### Load (Carga)
- Bulk insert via `INSERT ... ON CONFLICT DO NOTHING` (PostgreSQL nativo)
- Processamento em chunks de 5.000 registros para performance
- Conversão automática de valores `NaT`/`NaN` para `NULL`
- Relatório de estatísticas finais (inseridos por tabela)

### Script de Carga

```bash
python scripts/carregar_rapido.py
```

Carrega o dataset completo (~315k registros) em segundos usando bulk inserts com conflito ignorado automaticamente.

## 🎨 Dashboard Interativo

O dashboard React implementa um **design SaaS moderno** com tema escuro/claro, sidebar fixa no estilo Vision UI e glassmorphism.

### Sidebar

- Fixa, sempre visível, inspirada em Vision UI Dashboard
- Ícones com gradientes distintos por seção
- Card de usuário com indicador de status online
- Card "Precisa de ajuda?" com atalho direto ao Assistente IA
- Toggle dark/light mode

### 4 Páginas Analíticas

## 1. Visão Executiva
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/71dffe4c-5695-4ba9-8e37-4ba6ff92e0d1" />


- **4 KPIs principais** em cards: Receita Total, Pedidos, Clientes Únicos, Ticket Médio
- **Gráfico de área:** Evolução mensal da receita
- **Gráfico de barra:** Receita por estado
- Filtro de período interativo

## 2. Análise de Produtos
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e5ecf4cd-1b59-4944-a778-f387667b2184" />


- **Top N Produtos** por faturamento com nome legível (categoria + ID curto)
- **Top N Categorias** por faturamento (gráfico horizontal)
- **Gráfico de pizza:** Distribuição de receita por categoria
- **Gráfico de barra:** Volume por categoria
- Slider para ajustar N (5 a 20)

## 3. Clientes e Geografia
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/416e834b-81d7-46c4-9714-6277adebd2cf" />


- **Distribuição por estado:** Pedidos e receita por UF
- **Gráfico de pizza:** Distribuição por método de pagamento
- Seletor multiestado para filtro geográfico

## 4. Assistente IA
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/96ef8730-3fd9-4675-8fc9-9419c3172352" />


- **Chat interface** para consultas em linguagem natural
- **Exibição do SQL gerado** e dados brutos retornados
- **Exemplos de perguntas** para orientação

### Exemplos de Consultas via IA

- "Qual estado gerou mais receita?"
- "Qual categoria vendeu mais?"
- "Qual produto teve maior faturamento?"
- "Qual método de pagamento é mais utilizado?"
- "Quantos pedidos ocorreram em janeiro?"

### Tecnologias de Visualização

- **Recharts:** Gráficos responsivos (AreaChart, BarChart, PieChart)
- **Framer Motion:** Animações e transições
- **Tailwind CSS v4:** Estilização utility-first com tema customizado
- **CSS custom properties:** Suporte a dark/light mode

## 🤖 Assistente de IA com LangChain

O sistema implementa um assistente de dados usando **LangChain** e **Groq API** para consultas em linguagem natural.

### Arquitetura da IA

```
Usuário (pergunta em linguagem natural)
    ↓
LangChain SQL Chain (LCEL otimizado)
    ↓
LLM (llama-3.3-70b-versatile)
    ↓
SQL gerado
    ↓
PostgreSQL (execução)
    ↓
Resultados
    ↓
LLM (formatação)
    ↓
Resposta em linguagem natural
```

### Otimizações Implementadas

- **LCEL (LangChain Expression Language):** Chains modernas e eficientes
- **Cache automático:** Evita chamadas repetidas ao LLM
- **Prompts concisos:** Reduz consumo de tokens
- **Timeout configurado:** 30 segundos para evitar travamentos
- **max_tokens limitado:** 500 tokens para respostas rápidas
- **Modelo otimizado:** llama-3.3-70b-versatile (alta performance)

### Funcionalidades

- Geração automática de SQL a partir de perguntas em português
- Execução segura de queries no PostgreSQL
- Formatação de resultados em linguagem natural
- Exibição do SQL gerado para transparência
- Exibição dos dados brutos para auditoria
- Histórico de conversas na sessão

## 📈 KPIs Calculados

O sistema calcula automaticamente os seguintes indicadores de negócio:

### KPIs Financeiros
- **Receita Total:** Soma de todos os valores de pedidos (preço + frete)
- **Ticket Médio:** Receita total / Número de pedidos
- **Receita por Estado:** Distribuição geográfica de faturamento
- **Receita por Mês:** Evolução temporal de receita

### KPIs de Vendas
- **Número de Pedidos:** Total de pedidos realizados
- **Clientes Únicos:** Base de clientes distintos
- **Pedidos por Cliente:** Média de pedidos por cliente

### KPIs de Produtos
- **Top 10 Produtos:** Ranking por faturamento
- **Top 10 Categorias:** Ranking por faturamento
- **Quantidade por Categoria:** Volume de vendas por categoria

### KPIs de Pagamento
- **Métodos de Pagamento:** Distribuição por tipo (credit_card, boleto, voucher, debit_card)
- **Valor por Método:** Faturamento por tipo de pagamento

### KPIs Geográficos
- **Pedidos por Estado:** Distribuição de pedidos por UF
- **Receita por Estado:** Faturamento por UF

## 🚀 Instalação e Uso

### Pré-requisitos

- **Python 3.12+**
- **PostgreSQL 14+** (instalado localmente)
- **GROQ_API_KEY** (obtenha em https://groq.com)

### Instalação Manual

```bash
# 1. Clone o repositório
git clone <repo-url>
cd dados_aug

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais PostgreSQL e GROQ_API_KEY

# 6. Inicie PostgreSQL e crie banco de dados
createdb olist_db

# 7. Carregue o dataset Olist
python scripts/carregar_rapido.py

# 8. Inicie o backend (terminal 1)
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

# 9. Instale dependências do frontend React (terminal 2)
cd frontend-react
npm install

# 10. Inicie o frontend React
npm run dev
```

### Instalação Automatizada (Windows)

```powershell
.\start_dashboard.ps1
```

### Acessos

- **Frontend React:** http://localhost:3000
- **API:** http://localhost:8000
- **Documentação API (Swagger):** http://localhost:8000/docs
- **Documentação API (ReDoc):** http://localhost:8000/redoc

## 📚 Documentação Técnica

O projeto possui documentação técnica detalhada em `/docs`:

- **[docs/arquitetura.md](docs/arquitetura.md)** - Diagrama de arquitetura, camadas do sistema, padrões de projeto e fluxo de dados
- **[docs/dataset_olist_analysis.md](docs/dataset_olist_analysis.md)** - Análise completa do schema Olist, ERD, relacionamentos, KPIs possíveis e design do banco PostgreSQL
- **[docs/api_documentation.md](docs/api_documentation.md)** - Documentação completa da API REST com todos os endpoints, schemas e exemplos
- **[docs/auditoria_projeto.md](docs/auditoria_projeto.md)** - Auditoria técnica do projeto, estrutura de arquivos, funcionalidades implementadas e plano de migração

## ⚙️ Funcionalidades Principais

### Backend (FastAPI)
- ✅ API REST com endpoints para KPIs e consultas analíticas
- ✅ Validação de dados com Pydantic
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ CORS configurado para integração com frontend
- ✅ Health check endpoint
- ✅ Repository Pattern para acesso a dados
- ✅ Service Layer para lógica de negócio

### Pipeline ETL
- ✅ Extração de 5 CSVs do dataset Olist
- ✅ Transformação com validação de tipos e tratamento de nulos
- ✅ Carga rápida via bulk insert com `ON CONFLICT DO NOTHING`
- ✅ Conversão automática de NaT/NaN para NULL
- ✅ Relatório de estatísticas finais por tabela

### Banco de Dados
- ✅ Schema normalizado com 5 tabelas relacionais
- ✅ Chaves primárias e estrangeiras
- ✅ Índices para performance
- ✅ Constraints para integridade
- ✅ Conexão via SQLAlchemy ORM

### Inteligência Artificial
- ✅ LangChain com LCEL otimizado
- ✅ Integração com Groq API (llama-3.3-70b-versatile)
- ✅ Geração de SQL a partir de linguagem natural
- ✅ Execução segura de queries
- ✅ Formatação de respostas em português
- ✅ Cache automático para performance

### Frontend (React + Vite + TypeScript)
- ✅ SPA com React Router v6 e 4 páginas analíticas
- ✅ Design Vision UI com sidebar fixa e glassmorphism
- ✅ Dark/light mode com toggle
- ✅ Gráficos interativos com Recharts
- ✅ KPIs em cards com métricas principais
- ✅ Animações com Framer Motion
- ✅ Chat interface para consultas via IA
- ✅ Exibição de SQL gerado e dados brutos
- ✅ Top produtos com nome legível (categoria + ID curto)

## 🧪 Testes

O projeto inclui testes unitários e de integração:

```bash
# Executar todos os testes
pytest tests/

# Executar com coverage
pytest tests/ --cov=backend --cov=etl --cov=ai

# Executar testes específicos
pytest tests/unit/test_etl.py
pytest tests/unit/test_services.py
```

## 🎨 Formatação de Código

O projeto usa Black para formatação consistente do Python:

```bash
# Formatar todo o código
black backend/ etl/ ai/ tests/

# Verificar formatação sem modificar
black --check backend/ etl/ ai/ tests/
```

## 🔧 Variáveis de Ambiente

Configure as seguintes variáveis no arquivo `.env`:

```env
# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=olist_db
DB_USER=postgres
DB_PASSWORD=your_password

# IA (Groq)
AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key

# API
API_URL=http://localhost:8000
```

## 📝 Notas Importantes

- **Dataset Real:** O sistema utiliza o dataset Olist Brazilian E-Commerce do Kaggle, que contém dados reais de e-commerce brasileiro
- **Volume de Dados:** 100k+ registros distribuídos em 5 tabelas relacionais
- **Performance:** O pipeline ETL usa batch insert (1000 registros) para performance otimizada
- **IA:** O assistente usa Groq API com modelo llama-3.3-70b-versatile para alta performance e baixo custo
- **Arquitetura:** O sistema segue princípios SOLID e padrões de projeto profissionais (Repository, Service, DTO)


---

**Desenvolvido com Python, FastAPI, PostgreSQL, LangChain, React e Vite**
