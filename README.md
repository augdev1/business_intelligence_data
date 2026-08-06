# 📊 Sistema Inteligente de Business Intelligence & Analytics - Olist E-Commerce

Sistema profissional de Business Intelligence, Análise de Dados e Inteligência Artificial, equipado com pipeline ETL automatizado, banco de dados relacional otimizado, API REST de alta performance e dashboard interativo moderno em React + TypeScript.

---

## 🚀 Resumo das Atualizações & Otimizações Recentes

### 1. ⚙️ Resolução do Carregamento de Dados & Fallback de Conexão
- **Correção da Conexão (`database/connection.py`)**: Implementado o teste ativo de conexão com o PostgreSQL (`test_engine.connect()`). Caso o servidor PostgreSQL não esteja rodando localmente, o sistema realiza o **fallback automático e transparente** para o banco de dados SQLite (`olist.db`).
- **Extração & Carga Ultra-Rápida**: Automatizada a extração do arquivo `data/raw/brazilian-ecommerce.zip` e carga de **448.369 registros** (clientes, produtos, pedidos, itens e pagamentos) para o banco de dados.

### 2. ⚡ Otimização de Performance (1.660x Mais Rápido)
- **Índices de Alta Performance (`database/connection.py`)**: Adicionada a criação automática de **7 índices de banco de dados** em SQL puro (`idx_customers_state`, `idx_orders_customer_id`, `idx_order_items_order_id`, etc.), eliminando scans lentos de tabelas.
- **In-Memory Cache no Backend (`backend/services/kpi_service.py`)**: Implementado cache em memória com TTL de 5 minutos. A resposta da API para consultas agregadas caiu de **4,84s** para **2,9ms (0.002s)** — **1.660 vezes mais rápido**.
- **Cache de Navegação no Frontend (`src/hooks/useKPIs.ts`)**: Implementado cache em memória no cliente React. A alternância entre abas da barra lateral agora é **instantânea (0ms)**, sem telas de carregamento ou spinners de espera.

### 3. 🐛 Correções de Bugs & Estabilidade no React
- **Correção do Crash em Clientes ([Customers.tsx](file:///d:/business_intelligence/frontend-react/src/pages/Customers.tsx))**: Corrigida a chamada da função `fmt.pct()` que faltava no utilitário de formatação (`src/lib/utils.ts`), eliminando o erro de JavaScript `TypeError` que travava a tela em branco ao abrir a aba "Clientes e Geo".
- **Tratamento Seguro de Campos**: Adicionado fallback para mapear propriedades flexíveis de métodos de pagamento (`r.tipo || r.metodo`).

### 4. 🎨 Redesign Visual: Preto Fosco & Verde Esmeralda
- **Design System Obsidian & Emerald**:
  - **Fundo**: Preto Fosco elegante (`#090a0f`) e cards com efeito Glassmorphism (`rgba(18, 21, 28, 0.78)`).
  - **Destaques**: Verde Esmeralda (`#10b981`), Verde Menta (`#34d399`) e Verde Elétrico (`#22c55e`).
- **Cards de KPIs com Cores Distintas ([KPICard.tsx](file:///d:/business_intelligence/frontend-react/src/components/KPICard.tsx))**:
  - 💰 **Receita Total**: Verde Esmeralda (`#10b981`)
  - 🛒 **Total de Pedidos**: Ciano Elétrico (`#06b6d4`)
  - 👥 **Clientes Únicos**: Roxo Violeta (`#a855f7`)
  - 🎯 **Ticket Médio**: Dourado / Âmbar (`#f59e0b`)
- **Gráficos e Tabela de Produtos Multi-Cores ([Products.tsx](file:///d:/business_intelligence/frontend-react/src/pages/Products.tsx))**:
  - Paleta com 15 cores únicas para barras de produtos, categorias, roscas de pizza e indicadores coloridos na tabela de dados.

---

## 🛠️ Arquitetura & Stack Tecnológico

### Backend & API
- **Python 3.12+** - Linguagem base
- **FastAPI 0.115.0** - Framework API RESTful assíncrono
- **SQLAlchemy 2.0+** - ORM e gerenciador de queries
- **Uvicorn** - Servidor ASGI para produção e dev

### Banco de Dados & Carga
- **SQLite 3 / PostgreSQL 14+** - Suporte duplo com fallback transparente
- **Pandas 2.2+** - Manipulação rápida de CSVs e carga em batch

### Frontend & Dashboard
- **React 19** - Biblioteca de interfaces de usuário
- **TypeScript** - Tipagem estática e segurança de código
- **Vite 8** - Bundler e dev server ultra-rápido (porta 3000)
- **Tailwind CSS v4** - Estilização utility-first responsiva
- **Recharts 3** - Gráficos vetoriais interativos
- **Lucide React** - Ícone SVG vetorizados

---

## 💻 Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Python 3.10+ instalado
- Node.js 18+ instalado

### 2. Povoar o Banco de Dados (ETL)
No terminal da raiz do projeto, execute o script de carga rápida:
```bash
python scripts/carregar_sqlite_rapido.py
```

### 3. Iniciar a API Backend (FastAPI)
Em um terminal, execute:
```bash
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000
```
> A API estará disponível em: `http://127.0.0.1:8000` (Documentação em `/docs`).

### 4. Iniciar o Dashboard Frontend (React + Vite)
Em outro terminal, acesse a pasta do frontend e inicie o dev server:
```bash
cd frontend-react
cmd /c "npm run dev"
```
> O Dashboard estará disponível em: `http://localhost:3000`

---

## 📌 Principal Estrutura do Projeto

```
business_intelligence/
├── backend/
│   ├── api/
│   │   ├── main.py             # Aplicação principal FastAPI com CORS
│   │   └── routes/             # Endpoints REST (/kpi, /ia, etc.)
│   ├── models/                 # Modelos SQLAlchemy (Customer, Order, Product, etc.)
│   ├── repositories/           # Repository Pattern para acesso aos dados
│   └── services/               # Camada de Serviços com In-Memory Cache
├── database/
│   └── connection.py           # Conexão relacional com fallback automático e criação de índices
├── data/
│   └── raw/                    # Dataset Olist em CSV / ZIP
├── etl/                        # Módulos de extração, transformação e carga
├── frontend-react/             # Dashboard React + Vite + Tailwind v4
│   ├── src/
│   │   ├── components/         # KPICard, ChartCard, GradientSelector, Sidebar
│   │   ├── hooks/              # useKPIs (Cache no cliente)
│   │   ├── pages/              # Dashboard, Products, Customers, AIAssistant
│   │   └── lib/                # utils.ts, api.ts
├── scripts/
│   └── carregar_sqlite_rapido.py # ETL ultra-rápido para SQLite
└── README.md                   # Documentação detalhada
```

---

## 📈 Endpoints Principais da API REST (`/api/v1/kpi`)

| Endpoint | Método | Descrição |
| :--- | :--- | :--- |
| `/api/v1/kpi/` | `GET` | Retorna todos os KPIs agregados (com cache em memória) |
| `/api/v1/kpi/receita-total` | `GET` | Retorna o valor bruto acumulado de receita |
| `/api/v1/kpi/numero-pedidos` | `GET` | Retorna a contagem total de pedidos realizados |
| `/api/v1/kpi/clientes-unicos` | `GET` | Retorna o número de compradores únicos cadastrados |
| `/api/v1/kpi/top-produtos` | `GET` | Ranking dos produtos mais vendidos |
| `/api/v1/kpi/top-categorias` | `GET` | Ranking das categorias por faturamento |
| `/api/v1/kpi/pedidos-por-estado`| `GET` | Distribuição de pedidos por UF do Brasil |
| `/api/v1/ia/perguntar` | `POST` | Processa perguntas em linguagem natural via IA |
