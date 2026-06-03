# FASE 1 - Auditoria do Projeto

## 1. Estrutura do Projeto Atual

### 1.1 Arquivos Existentes

```
d:\dados_aug/
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── ai/
│   ├── __init__.py
│   ├── prompts.py
│   └── sql_chain.py
├── backend/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── ia.py
│   │   │   ├── indicadores.py
│   │   │   └── vendas.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── vendas.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── venda.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── venda_repository.py
│   └── services/
│       ├── __init__.py
│       ├── ia_service.py
│       ├── indicador_service.py
│       └── venda_service.py
├── data/
│   └── raw/
│       ├── .gitkeep
│       ├── olist_customers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       ├── product_category_name_translation.csv
│       └── brazilian-ecommerce.zip
├── database/
│   ├── __init__.py
│   └── connection.py
├── docs/
│   ├── arquitetura.md
│   ├── dataset_olist_analysis.md
│   └── guia_instalacao.md
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── etl/
│   ├── __init__.py
│   ├── extract.py
│   ├── load.py
│   └── transform.py
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   └── pages/
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── integration/
    │   └── __init__.py
    └── unit/
        ├── __init__.py
        ├── test_etl.py
        └── test_services.py
```

**Total de arquivos Python:** 29
**Total de arquivos de documentação:** 3
**Total de arquivos CSV Olist:** 9 (já baixados)

---

## 2. Funcionalidades Atuais

### 2.1 Funcionalidades JÁ IMPLEMENTADAS

**Backend (FastAPI):**
- ✅ API REST funcional com rotas para vendas, indicadores e IA
- ✅ Upload de CSV (schema simples: id_venda, data_venda, produto, categoria, cidade, quantidade, valor_unitario)
- ✅ Cálculo de indicadores básicos (faturamento, quantidade, ticket médio)
- ✅ Ranking de produtos e cidades
- ✅ Evolução mensal de vendas
- ✅ Integração com LangChain para consultas em linguagem natural
- ✅ Suporte a OpenAI e Groq como providers de IA

**ETL:**
- ✅ Pipeline ETL funcional (extract, transform, load)
- ✅ Validação de colunas e tipos de dados
- ✅ Tratamento de duplicatas e valores nulos
- ✅ Carga em batch no PostgreSQL

**Frontend (Streamlit):**
- ✅ Dashboard com 3 páginas (Dashboard, Upload CSV, Assistente IA)
- ✅ KPIs principais (faturamento, quantidade, ticket médio)
- ✅ Gráficos interativos (evolução mensal, rankings)
- ✅ Chat interface para consultas via IA
- ✅ Upload de CSV com pré-visualização

**Banco de Dados:**
- ✅ Conexão PostgreSQL configurada
- ✅ Modelo SQLAlchemy para tabela `vendas`
- ✅ Repository pattern implementado
- ✅ Service layer implementado

**IA:**
- ✅ LangChain configurado com LCEL (otimizado)
- ✅ Cache em memória para performance
- ✅ Suporte a OpenAI (gpt-4o-mini) e Groq (llama-3.1-70b-versatile)
- ✅ Geração de SQL a partir de linguagem natural
- ✅ Formatação de respostas

---

## 3. Problemas Identificados

### 3.1 Schema de Dados

**Problema Crítico:**
- O sistema atual usa uma tabela única `vendas` com schema simplificado
- O dataset Olist possui 5 tabelas principais com relacionamentos complexos
- Não há compatibilidade entre o schema atual e o schema Olist

**Impacto:**
- Todo o modelo de dados precisa ser refeito
- Repositories precisam ser reescritos
- Services precisam ser adaptados
- ETL precisa ser completamente refeito
- IA precisa ser reconfigurada com novo schema

### 3.2 Arquitetura

**Pontos Positivos:**
- ✅ Arquitetura em camadas bem definida (API → Service → Repository → ORM)
- ✅ Repository pattern implementado corretamente
- ✅ Service layer separando lógica de negócio
- ✅ ETL modular (extract, transform, load)
- ✅ IA desacoplada com LangChain

**Pontos a Melhorar:**
- ⚠️ Modelo de dados monolítico (tabela única) não suporta e-commerce real
- ⚠️ Falta de models para as tabelas do Olist
- ⚠️ Repositories acoplados ao modelo Venda
- ⚠️ Services acoplados ao VendaRepository
- ⚠️ IA com schema hard-coded no prompt

### 3.3 Dependências

**Status:**
- ✅ FastAPI configurado
- ✅ SQLAlchemy configurado
- ✅ Streamlit configurado
- ✅ LangChain configurado
- ✅ PostgreSQL configurado
- ✅ Pandas instalado

---

## 4. O que Precisa ser Adaptado para Olist

### 4.1 Modelos SQLAlchemy (NOVO)

**Arquivos a CRIAR:**
- `backend/models/customer.py`
- `backend/models/product.py`
- `backend/models/order.py`
- `backend/models/order_item.py`
- `backend/models/order_payment.py`

**Arquivo a MODIFICAR:**
- `backend/models/__init__.py` - Importar novos modelos

**Arquivo a DELETAR:**
- `backend/models/venda.py` - Substituído pelos novos modelos

### 4.2 Repositories (NOVO)

**Arquivos a CRIAR:**
- `backend/repositories/customer_repository.py`
- `backend/repositories/product_repository.py`
- `backend/repositories/order_repository.py`
- `backend/repositories/order_item_repository.py`
- `backend/repositories/order_payment_repository.py`
- `backend/repositories/kpi_repository.py` - Para consultas analíticas complexas

**Arquivos a MODIFICAR:**
- `backend/repositories/__init__.py` - Importar novos repositories

**Arquivo a DELETAR:**
- `backend/repositories/venda_repository.py` - Substituído pelos novos repositories

### 4.3 Services (ADAPTAR)

**Arquivos a MODIFICAR:**
- `backend/services/venda_service.py` - Renomear para `order_service.py` e adaptar
- `backend/services/indicador_service.py` - Adaptar para usar novos repositories e KPIs Olist
- `backend/services/ia_service.py` - Adaptar para usar novo schema

**Arquivos a CRIAR:**
- `backend/services/kpi_service.py` - Serviço dedicado para KPIs Olist

### 4.4 API Routes (ADAPTAR)

**Arquivos a MODIFICAR:**
- `backend/api/routes/vendas.py` - Renomear para `orders.py` e adaptar endpoints
- `backend/api/routes/indicadores.py` - Adaptar para novos KPIs Olist
- `backend/api/main.py` - Atualizar imports

**Arquivos a CRIAR:**
- `backend/api/routes/kpi.py` - Rotas específicas para KPIs Olist

**Arquivos a MODIFICAR:**
- `backend/api/schemas/vendas.py` - Renomear para `orders.py` e criar novos schemas

### 4.5 ETL (REFAZER)

**Arquivos a CRIAR:**
- `etl/extract_olist.py` - Extração específica para 5 CSVs Olist
- `etl/transform_olist.py` - Transformação específica para Olist
- `etl/load_olist.py` - Carga específica para Olist

**Arquivos a MODIFICAR:**
- `etl/__init__.py` - Exportar novas funções

**Arquivos a DELETAR:**
- `etl/extract.py` - Substituído por extract_olist.py
- `etl/transform.py` - Substituído por transform_olist.py
- `etl/load.py` - Substituído por load_olist.py

### 4.6 IA (RECONFIGURAR)

**Arquivos a MODIFICAR:**
- `ai/sql_chain.py` - Atualizar schema no prompt para 5 tabelas Olist
- `ai/prompts.py` - Atualizar templates para novo schema

### 4.7 Frontend (REFAZER)

**Arquivos a MODIFICAR:**
- `frontend/app.py` - Refazer completamente com 4 páginas e design moderno SaaS

**Arquivos a CRIAR:**
- `frontend/pages/executive.py` - Página Visão Executiva
- `frontend/pages/products.py` - Página Produtos
- `frontend/pages/geography.py` - Página Clientes e Geografia
- `frontend/pages/assistant.py` - Página Assistente IA

### 4.8 Banco de Dados (ATUALIZAR)

**Arquivos a MODIFICAR:**
- `database/connection.py` - Atualizar para criar novas tabelas

---

## 5. Resumo de Modificações

### 5.1 Arquivos a CRIAR (15)

**Models (5):**
- backend/models/customer.py
- backend/models/product.py
- backend/models/order.py
- backend/models/order_item.py
- backend/models/order_payment.py

**Repositories (6):**
- backend/repositories/customer_repository.py
- backend/repositories/product_repository.py
- backend/repositories/order_repository.py
- backend/repositories/order_item_repository.py
- backend/repositories/order_payment_repository.py
- backend/repositories/kpi_repository.py

**Services (1):**
- backend/services/kpi_service.py

**API (2):**
- backend/api/routes/kpi.py
- backend/api/routes/orders.py (renomeado de vendas.py)

**ETL (3):**
- etl/extract_olist.py
- etl/transform_olist.py
- etl/load_olist.py

**Frontend (4):**
- frontend/pages/executive.py
- frontend/pages/products.py
- frontend/pages/geography.py
- frontend/pages/assistant.py

### 5.2 Arquivos a MODIFICAR (10)

- backend/models/__init__.py
- backend/repositories/__init__.py
- backend/services/venda_service.py → order_service.py
- backend/services/indicador_service.py
- backend/services/ia_service.py
- backend/api/main.py
- backend/api/routes/indicadores.py
- backend/api/schemas/vendas.py → orders.py
- ai/sql_chain.py
- ai/prompts.py
- frontend/app.py
- database/connection.py

### 5.3 Arquivos a DELETAR (6)

- backend/models/venda.py
- backend/repositories/venda_repository.py
- etl/extract.py
- etl/transform.py
- etl/load.py

### 5.4 Arquivos a MANTER (SEM ALTERAÇÃO)

- backend/api/routes/ia.py (apenas atualizar imports)
- backend/repositories/base.py
- backend/api/main.py (apenas atualizar imports)
- docs/arquitetura.md
- docs/dataset_olist_analysis.md
- docs/guia_instalacao.md
- README.md
- requirements.txt
- pyproject.toml
- .env.example
- .gitignore

---

## 6. Plano de Migração

### Fase 1 - Modelagem (FASE 2 do projeto)
1. Criar 5 modelos SQLAlchemy com relacionamentos corretos
2. Definir PKs e FKs conforme dataset Olist
3. Implementar relacionamentos ORM (relationship)

### Fase 2 - Banco de Dados (FASE 3 do projeto)
1. Atualizar connection.py para criar novas tabelas
2. Criar índices para performance
3. Criar constraints para integridade

### Fase 3 - ETL (FASE 4 do projeto)
1. Criar extract_olist.py para ler 5 CSVs
2. Criar transform_olist.py para validar e transformar
3. Criar load_olist.py para carregar em batch
4. Implementar logs e tratamento de erros

### Fase 4 - Repositories & Services (FASE 5 do projeto)
1. Criar 6 repositories específicos
2. Criar kpi_repository para consultas analíticas
3. Criar kpi_service para cálculo de indicadores
4. Adaptar services existentes

### Fase 5 - API (FASE 5 do projeto)
1. Criar rotas para KPIs Olist
2. Adaptar rotas de indicadores
3. Atualizar schemas Pydantic

### Fase 6 - IA (FASE 7 do projeto)
1. Atualizar schema no prompt LangChain
2. Configurar para usar Groq (llama-3.3-70b-versatile)
3. Testar consultas

### Fase 7 - Dashboard (FASE 6 do projeto)
1. Refazer frontend com design SaaS moderno
2. Implementar 4 páginas separadas
3. Modo escuro elegante
4. Gráficos profissionais

### Fase 8 - Validação (FASE 8 do projeto)
1. Testar todas as consultas
2. Validar KPIs
3. Validar IA
4. Gerar relatório final

---

## 7. Riscos e Mitigações

### Risco 1: Perda de funcionalidade existente
**Mitigação:** Manter arquivos antigos como backup até migração completa

### Risco 2: Complexidade do schema Olist
**Mitigação:** Seguir estritamente a documentação do dataset, não inventar colunas

### Risco 3: Performance com 5 tabelas
**Mitigação:** Criar índices adequados, usar views para consultas complexas

### Risco 4: IA com schema complexo
**Mitigação:** Simplificar prompt, fornecer exemplos claros, testar exaustivamente

---

## 8. Conclusão

**Status Atual:** Sistema funcional mas com schema simplificado inadequado para e-commerce real.

**Necessidade:** Migração completa para dataset Olist é essencial para portfólio profissional.

**Complexidade:** Alta - requer reescrita de models, repositories, services, ETL, IA e frontend.

**Tempo Estimado:** 8 fases conforme plano detalhado.

**Próximo Passo:** Aguardar aprovação desta auditoria para iniciar FASE 2 - Modelagem Olist.

---

**Documento criado em:** 2026-06-03  
**Versão:** 1.0  
**Status:** Aguardando aprovação
