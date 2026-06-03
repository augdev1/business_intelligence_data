# Análise do Dataset Olist Brazilian E-Commerce

## Fonte Oficial de Dados

**Dataset:** Olist Brazilian E-Commerce  
**URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
**Licença:** CC-BY-NC-SA-4.0

## Arquivos CSV Analisados

Os seguintes arquivos foram baixados e analisados:
- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_products_dataset.csv`
- `olist_order_payments_dataset.csv`

---

## 1. Estrutura das Tabelas

### 1.1 Tabela: customers (olist_customers_dataset.csv)

**Colunas:**
- `customer_id` (VARCHAR) - Identificador único do cliente
- `customer_unique_id` (VARCHAR) - Identificador único do cliente (agregado)
- `customer_zip_code_prefix` (INTEGER) - Prefixo do CEP
- `customer_city` (VARCHAR) - Cidade do cliente
- `customer_state` (VARCHAR) - Estado do cliente (UF)

**Chave Primária (PK):** `customer_id`

**Registros:** 99,441

**Observações:** Não há valores nulos nesta tabela.

---

### 1.2 Tabela: orders (olist_orders_dataset.csv)

**Colunas:**
- `order_id` (VARCHAR) - Identificador único do pedido
- `customer_id` (VARCHAR) - Identificador do cliente (FK)
- `order_status` (VARCHAR) - Status do pedido (created, approved, delivered, etc.)
- `order_purchase_timestamp` (TIMESTAMP) - Data/hora da compra
- `order_approved_at` (TIMESTAMP) - Data/hora da aprovação
- `order_delivered_carrier_date` (TIMESTAMP) - Data/hora de entrega ao transportador
- `order_delivered_customer_date` (TIMESTAMP) - Data/hora de entrega ao cliente
- `order_estimated_delivery_date` (DATE) - Data estimada de entrega

**Chave Primária (PK):** `order_id`

**Chave Estrangeira (FK):** `customer_id` → customers.customer_id

**Registros:** 99,441

**Valores Nulos:**
- `order_approved_at`: 160 registros
- `order_delivered_carrier_date`: 1,783 registros
- `order_delivered_customer_date`: 2,965 registros

---

### 1.3 Tabela: order_items (olist_order_items_dataset.csv)

**Colunas:**
- `order_id` (VARCHAR) - Identificador do pedido (FK)
- `order_item_id` (INTEGER) - Número sequencial do item no pedido
- `product_id` (VARCHAR) - Identificador do produto (FK)
- `seller_id` (VARCHAR) - Identificador do vendedor (FK)
- `shipping_limit_date` (DATE) - Data limite de envio
- `price` (DECIMAL) - Preço do item
- `freight_value` (DECIMAL) - Valor do frete

**Chave Primária (PK):** (`order_id`, `order_item_id`) - Chave composta

**Chaves Estrangeiras (FK):**
- `order_id` → orders.order_id
- `product_id` → products.product_id
- `seller_id` → sellers.seller_id

**Registros:** 112,650

**Observações:** Não há valores nulos. Um pedido pode ter múltiplos itens.

---

### 1.4 Tabela: products (olist_products_dataset.csv)

**Colunas:**
- `product_id` (VARCHAR) - Identificador único do produto
- `product_category_name` (VARCHAR) - Categoria do produto (em português)
- `product_name_lenght` (INTEGER) - Comprimento do nome do produto
- `product_description_lenght` (INTEGER) - Comprimento da descrição
- `product_photos_qty` (INTEGER) - Quantidade de fotos
- `product_weight_g` (INTEGER) - Peso do produto em gramas
- `product_length_cm` (INTEGER) - Comprimento em cm
- `product_height_cm` (INTEGER) - Altura em cm
- `product_width_cm` (INTEGER) - Largura em cm

**Chave Primária (PK):** `product_id`

**Registros:** 32,951

**Valores Nulos:**
- `product_category_name`: 610 registros
- `product_name_lenght`: 610 registros
- `product_description_lenght`: 610 registros
- `product_photos_qty`: 610 registros
- `product_weight_g`: 2 registros
- `product_length_cm`: 2 registros
- `product_height_cm`: 2 registros
- `product_width_cm`: 2 registros

---

### 1.5 Tabela: order_payments (olist_order_payments_dataset.csv)

**Colunas:**
- `order_id` (VARCHAR) - Identificador do pedido (FK)
- `payment_sequential` (INTEGER) - Sequencial do pagamento
- `payment_type` (VARCHAR) - Tipo de pagamento (credit_card, boleto, voucher, debit_card)
- `payment_installments` (INTEGER) - Número de parcelas
- `payment_value` (DECIMAL) - Valor do pagamento

**Chave Primária (PK):** (`order_id`, `payment_sequential`) - Chave composta

**Chave Estrangeira (FK):** `order_id` → orders.order_id

**Registros:** 103,886

**Observações:** Não há valores nulos. Um pedido pode ter múltiplos pagamentos.

---

## 2. Diagrama Entidade-Relacionamento (ERD)

```
┌─────────────────────────────────────────────────────────────┐
│                        CUSTOMERS                              │
├─────────────────────────────────────────────────────────────┤
│ PK  customer_id              VARCHAR                         │
│     customer_unique_id       VARCHAR                         │
│     customer_zip_code_prefix INTEGER                         │
│     customer_city            VARCHAR                         │
│     customer_state           VARCHAR                         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ 1
                              │
                              │ N
┌─────────────────────────────▼───────────────────────────────┐
│                         ORDERS                               │
├─────────────────────────────────────────────────────────────┤
│ PK  order_id                 VARCHAR                         │
│ FK  customer_id              VARCHAR                         │
│     order_status            VARCHAR                         │
│     order_purchase_timestamp TIMESTAMP                       │
│     order_approved_at        TIMESTAMP                       │
│     order_delivered_carrier_date TIMESTAMP                   │
│     order_delivered_customer_date TIMESTAMP                  │
│     order_estimated_delivery_date DATE                      │
└──────────────┬──────────────────────────────┬───────────────┘
               │ 1                            │ 1
               │                              │
               │ N                            │ N
┌──────────────▼──────────────┐  ┌──────────▼──────────────────┐
│       ORDER_ITEMS           │  │      ORDER_PAYMENTS         │
├─────────────────────────────┤  ├─────────────────────────────┤
│ FK  order_id      VARCHAR   │  │ FK  order_id      VARCHAR   │
│ PK  order_item_id INTEGER   │  │ PK  payment_sequential INTEGER│
│ FK  product_id    VARCHAR   │  │     payment_type   VARCHAR   │
│ FK  seller_id     VARCHAR   │  │     payment_installments INTEGER│
│     shipping_limit_date DATE│  │     payment_value  DECIMAL   │
│     price          DECIMAL  │  └─────────────────────────────┘
│     freight_value  DECIMAL  │
└──────────────┬──────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────┐
│        PRODUCTS             │
├─────────────────────────────┤
│ PK  product_id      VARCHAR  │
│     product_category_name VARCHAR│
│     product_name_lenght INTEGER │
│     product_description_lenght INTEGER│
│     product_photos_qty INTEGER   │
│     product_weight_g   INTEGER   │
│     product_length_cm  INTEGER   │
│     product_height_cm  INTEGER   │
│     product_width_cm   INTEGER   │
└─────────────────────────────┘
```

---

## 3. Relacionamentos Entre Tabelas

### 3.1 customers ↔ orders
- **Tipo:** 1:N (One-to-Many)
- **Descrição:** Um cliente pode fazer múltiplos pedidos, mas cada pedido pertence a apenas um cliente.
- **FK:** orders.customer_id → customers.customer_id

### 3.2 orders ↔ order_items
- **Tipo:** 1:N (One-to-Many)
- **Descrição:** Um pedido pode conter múltiplos itens, mas cada item pertence a apenas um pedido.
- **FK:** order_items.order_id → orders.order_id
- **PK Composta:** (order_id, order_item_id)

### 3.3 orders ↔ order_payments
- **Tipo:** 1:N (One-to-Many)
- **Descrição:** Um pedido pode ter múltiplos pagamentos (ex: parcelas, múltiplos métodos), mas cada pagamento pertence a apenas um pedido.
- **FK:** order_payments.order_id → orders.order_id
- **PK Composta:** (order_id, payment_sequential)

### 3.4 products ↔ order_items
- **Tipo:** 1:N (One-to-Many)
- **Descrição:** Um produto pode estar em múltiplos itens de pedido, mas cada item de pedido contém apenas um produto.
- **FK:** order_items.product_id → products.product_id

### 3.5 sellers ↔ order_items
- **Tipo:** 1:N (One-to-Many)
- **Descrição:** Um vendedor pode vender múltiplos produtos em múltiplos pedidos, mas cada item de pedido tem apenas um vendedor.
- **FK:** order_items.seller_id → sellers.seller_id
- **Nota:** A tabela sellers não está incluída nos 5 arquivos principais, mas é referenciada em order_items.

---

## 4. KPIs Possíveis

### 4.1 KPIs de Vendas
- **Faturamento Total:** Soma de todos os valores de pedidos
- **Quantidade de Pedidos:** Número total de pedidos realizados
- **Ticket Médio:** Faturamento total / Quantidade de pedidos
- **Valor Médio por Item:** Soma de preços / Quantidade de itens
- **Faturamento por Categoria:** Soma de valores agrupada por categoria de produto
- **Faturamento por Estado:** Soma de valores agrupada por estado do cliente

### 4.2 KPIs de Produto
- **Produtos Mais Vendidos:** Ranking por quantidade de itens vendidos
- **Categorias Mais Populares:** Ranking por quantidade de itens por categoria
- **Preço Médio por Categoria:** Média de preços por categoria
- **Produtos com Maior Faturamento:** Ranking por valor total vendido

### 4.3 KPIs de Pagamento
- **Distribuição por Tipo de Pagamento:** Percentual por tipo (credit_card, boleto, voucher, debit_card)
- **Média de Parcelas:** Número médio de parcelas por pedido
- **Valor Médio por Tipo de Pagamento:** Valor médio por tipo de pagamento

### 4.4 KPIs de Entrega
- **Taxa de Entrega no Prazo:** Pedidos entregues na data estimada
- **Tempo Médio de Entrega:** Média de dias entre compra e entrega
- **Taxa de Aprovação:** Pedidos aprovados / Pedidos criados

### 4.5 KPIs Geográficos
- **Vendas por Estado:** Distribuição de vendas por estado
- **Vendas por Cidade:** Top cidades por faturamento
- **Distribuição Regional:** Faturamento por região do Brasil

### 4.6 KPIs Temporais
- **Vendas Mensais:** Evolução de faturamento por mês
- **Vendas por Dia da Semana:** Distribuição de vendas por dia
- **Sazonalidade:** Padrões de vendas ao longo do ano

---

## 5. Métricas para Dashboard

### 5.1 Cards de KPIs (Topo)
- Faturamento Total (R$)
- Quantidade de Pedidos
- Ticket Médio (R$)
- Taxa de Entrega no Prazo (%)

### 5.2 Gráficos Principais
- **Linha:** Evolução mensal do faturamento
- **Barra:** Top 10 produtos mais vendidos
- **Barra:** Top 10 categorias por faturamento
- **Pizza:** Distribuição por tipo de pagamento
- **Mapa:** Distribuição geográfica das vendas por estado
- **Barra:** Vendas por dia da semana

### 5.3 Tabelas Detalhadas
- Ranking de produtos por faturamento
- Ranking de cidades por faturamento
- Lista de pedidos recentes com status

### 5.4 Filtros Interativos
- Período de data (compra, entrega)
- Estado/Cidade
- Categoria de produto
- Status do pedido
- Tipo de pagamento

---

## 6. Design do Banco PostgreSQL

### 6.1 Schema SQL

```sql
-- Tabela: customers
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix INTEGER NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_state VARCHAR(2) NOT NULL
);

CREATE INDEX idx_customers_unique_id ON customers(customer_unique_id);
CREATE INDEX idx_customers_state ON customers(customer_state);
CREATE INDEX idx_customers_city ON customers(customer_city);

-- Tabela: products
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g NUMERIC(10, 2),
    product_length_cm NUMERIC(10, 2),
    product_height_cm NUMERIC(10, 2),
    product_width_cm NUMERIC(10, 2)
);

CREATE INDEX idx_products_category ON products(product_category_name);

-- Tabela: orders
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    order_purchase_timestamp TIMESTAMP NOT NULL,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date DATE NOT NULL,
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_purchase_date ON orders(order_purchase_timestamp);
CREATE INDEX idx_orders_estimated_delivery ON orders(order_estimated_delivery_date);

-- Tabela: order_items
CREATE TABLE order_items (
    order_id VARCHAR(50) NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50),
    shipping_limit_date DATE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    freight_value NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_order_items_seller ON order_items(seller_id);

-- Tabela: order_payments
CREATE TABLE order_payments (
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type VARCHAR(20) NOT NULL,
    payment_installments INTEGER NOT NULL,
    payment_value NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_order_payments_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE INDEX idx_order_payments_type ON order_payments(payment_type);
```

### 6.2 Views para Consultas

```sql
-- View: Resumo de Pedidos
CREATE VIEW v_order_summary AS
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_city,
    c.customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    COUNT(oi.order_item_id) as total_items,
    SUM(oi.price + oi.freight_value) as total_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, c.customer_city, c.customer_state;

-- View: Produtos por Categoria
CREATE VIEW v_products_by_category AS
SELECT 
    p.product_category_name,
    COUNT(DISTINCT p.product_id) as total_products,
    COUNT(oi.order_item_id) as total_items_sold,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_category_name;

-- View: Vendas por Estado
CREATE VIEW v_sales_by_state AS
SELECT 
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(oi.price + oi.freight_value) as avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_state;
```

---

## 7. Arquitetura de Dados

### 7.1 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    Kaggle Dataset                            │
│              (CSV Files - Olist E-commerce)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Download
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    data/raw/                                 │
│              CSV Files Originais                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ ETL Pipeline
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ETL Layer                                 │
│  - Extract: Leitura dos CSVs                               │
│  - Transform: Limpeza, validação, tipagem                  │
│  - Load: Inserção no PostgreSQL                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                         │
│  - customers                                                │
│  - products                                                 │
│  - orders                                                   │
│  - order_items                                              │
│  - order_payments                                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Queries
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Business Logic Layer (Services)                 │
│  - Cálculo de KPIs                                          │
│  - Agregações temporais                                     │
│  - Filtros dinâmicos                                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ API REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Layer (FastAPI)                        │
│  - Endpoints para indicadores                               │
│  - Endpoints para filtros                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Frontend (Streamlit)                        │
│  - Dashboard interativo                                     │
│  - Gráficos e visualizações                                 │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Estrutura de Diretórios Atualizada

```
d:\dados_aug/
├── data/
│   ├── raw/                    # CSVs originais do Olist
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   └── olist_order_payments_dataset.csv
│   └── processed/              # Dados processados (se necessário)
├── backend/
│   ├── models/                 # Modelos SQLAlchemy atualizados
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── order_payment.py
│   ├── repositories/           # Repositories atualizados
│   │   ├── customer_repository.py
│   │   ├── product_repository.py
│   │   ├── order_repository.py
│   │   └── ...
│   └── services/               # Services de KPIs
│       ├── kpi_service.py
│       └── ...
├── etl/
│   ├── extract_olist.py        # Extração específica Olist
│   ├── transform_olist.py      # Transformação específica Olist
│   └── load_olist.py           # Carga específica Olist
└── docs/
    └── dataset_olist_analysis.md  # Este documento
```

### 7.3 Estratégia de ETL

**Extract:**
- Leitura dos 5 arquivos CSV principais
- Validação de schema (colunas e tipos)
- Detecção de valores nulos e outliers

**Transform:**
- Conversão de tipos (strings para datas, números)
- Tratamento de valores nulos (preenchimento ou exclusão)
- Normalização de categorias de produtos
- Cálculo de campos derivados (ex: total_order_value)

**Load:**
- Inserção em lote (batch insert) para performance
- Uso de transações para garantir integridade
- Criação de índices após carga
- Validação de integridade referencial

### 7.4 Considerações de Performance

- **Índices:** Criar índices nas colunas frequentemente usadas em filtros e joins
- **Particionamento:** Considerar particionamento da tabela orders por data
- **Materialized Views:** Para KPIs que não mudam frequentemente
- **Cache:** Cache de resultados de consultas pesadas no backend
- **Query Optimization:** Usar EXPLAIN ANALYZE para otimizar queries

---

## 8. Próximos Passos (Aguardando Aprovação)

Após aprovação desta arquitetura, os seguintes passos serão implementados:

1. **Atualizar modelos SQLAlchemy** para refletir o schema do Olist
2. **Criar scripts ETL específicos** para o dataset Olist
3. **Implementar services de KPIs** baseados nas métricas definidas
4. **Atualizar o frontend** com novos gráficos e filtros
5. **Criar migrações do banco** para o novo schema
6. **Testar o pipeline ETL** com os dados reais
7. **Validar KPIs** contra o dataset original

---

## 9. Notas Importantes

- **Integridade Referencial:** A tabela `sellers` é referenciada em `order_items` mas não está nos 5 arquivos principais. Será necessário incluir `olist_sellers_dataset.csv` se quisermos analisar dados de vendedores.
- **Valores Nulos:** Algumas colunas têm valores nulos (especialmente em products e orders). Isso deve ser tratado no ETL.
- **Tradução de Categorias:** Existe um arquivo `product_category_name_translation.csv` que pode ser usado para traduzir categorias de português para inglês.
- **Geolocalização:** O arquivo `olist_geolocation_dataset.csv` pode ser usado para enriquecer dados geográficos, mas não é essencial para os KPIs principais.
- **Reviews:** O arquivo `olist_order_reviews_dataset.csv` pode ser usado para análise de sentimentos, mas não é essencial para KPIs de vendas.

---

**Documento criado em:** 2026-06-03  
**Versão:** 1.0  
**Status:** Aguardando aprovação da arquitetura
