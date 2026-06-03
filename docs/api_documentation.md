# Documentação da API

## Base URL

```
http://localhost:8000
```

## Autenticação

Atualmente não há autenticação implementada. Em produção, deve ser adicionada JWT ou OAuth2.

## Endpoints

### Vendas

#### Upload CSV

Faz upload e processa um arquivo CSV de vendas.

```http
POST /api/v1/vendas/upload
Content-Type: multipart/form-data
```

**Parâmetros:**
- `file` (file, required): Arquivo CSV

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "CSV processado com sucesso",
  "estatisticas": {
    "total_registros": 100,
    "carregados": 95,
    "duplicatas": 5,
    "erros": 0
  },
  "erros": [],
  "avisos": ["5 registros duplicados removidos"]
}
```

#### Listar Vendas

Lista vendas com paginação.

```http
GET /api/v1/vendas/?skip=0&limit=100
```

**Parâmetros:**
- `skip` (integer, optional): Quantidade de registros para pular (default: 0)
- `limit` (integer, optional): Quantidade máxima de registros (default: 100)

**Resposta:**
```json
[
  {
    "id": 1,
    "id_venda": "V001",
    "data_venda": "2024-01-01",
    "produto": "Produto A",
    "categoria": "Categoria A",
    "cidade": "São Paulo",
    "quantidade": 10,
    "valor_unitario": 100.00,
    "faturamento": 1000.00
  }
]
```

#### Obter Venda por ID

Busca uma venda específica.

```http
GET /api/v1/vendas/{venda_id}
```

**Parâmetros:**
- `venda_id` (integer, required): ID da venda

**Resposta:**
```json
{
  "id": 1,
  "id_venda": "V001",
  "data_venda": "2024-01-01",
  "produto": "Produto A",
  "categoria": "Categoria A",
  "cidade": "São Paulo",
  "quantidade": 10,
  "valor_unitario": 100.00,
  "faturamento": 1000.00
}
```

#### Contar Vendas

Conta o total de vendas no banco.

```http
GET /api/v1/vendas/contagem/total
```

**Resposta:**
```json
{
  "total": 1000
}
```

### Indicadores

#### Todos os Indicadores

Retorna todos os indicadores de negócio calculados.

```http
GET /api/v1/indicadores/
```

**Resposta:**
```json
{
  "faturamento_total": 100000.00,
  "quantidade_total": 1000,
  "ticket_medio": 100.00,
  "produto_mais_vendido": {
    "produto": "Produto A",
    "quantidade": 500
  },
  "categoria_mais_vendida": {
    "categoria": "Categoria A",
    "quantidade": 700
  },
  "cidade_maior_faturamento": {
    "cidade": "São Paulo",
    "faturamento": 50000.00
  },
  "evolucao_mensal": [
    {
      "ano": 2024,
      "mes": 1,
      "faturamento": 10000.00,
      "quantidade": 100
    }
  ],
  "ranking_produtos": [
    {
      "produto": "Produto A",
      "quantidade": 500,
      "faturamento": 50000.00
    }
  ],
  "ranking_cidades": [
    {
      "cidade": "São Paulo",
      "quantidade": 300,
      "faturamento": 50000.00
    }
  ],
  "total_vendas": 1000
}
```

#### Faturamento Total

```http
GET /api/v1/indicadores/faturamento-total
```

**Resposta:**
```json
{
  "faturamento_total": 100000.00
}
```

#### Quantidade Total

```http
GET /api/v1/indicadores/quantidade-total
```

**Resposta:**
```json
{
  "quantidade_total": 1000
}
```

#### Ticket Médio

```http
GET /api/v1/indicadores/ticket-medio
```

**Resposta:**
```json
{
  "ticket_medio": 100.00
}
```

#### Evolução Mensal

```http
GET /api/v1/indicadores/evolucao-mensal
```

**Resposta:**
```json
{
  "evolucao_mensal": [
    {
      "ano": 2024,
      "mes": 1,
      "faturamento": 10000.00,
      "quantidade": 100
    }
  ]
}
```

#### Ranking de Produtos

```http
GET /api/v1/indicadores/ranking-produtos?limit=10
```

**Parâmetros:**
- `limit` (integer, optional): Quantidade máxima de produtos (default: 10)

**Resposta:**
```json
{
  "ranking_produtos": [
    {
      "produto": "Produto A",
      "quantidade": 500,
      "faturamento": 50000.00
    }
  ]
}
```

#### Ranking de Cidades

```http
GET /api/v1/indicadores/ranking-cidades?limit=10
```

**Parâmetros:**
- `limit` (integer, optional): Quantidade máxima de cidades (default: 10)

**Resposta:**
```json
{
  "ranking_cidades": [
    {
      "cidade": "São Paulo",
      "quantidade": 300,
      "faturamento": 50000.00
    }
  ]
}
```

#### Vendas por Período

```http
GET /api/v1/indicadores/periodo?data_inicio=2024-01-01&data_fim=2024-12-31
```

**Parâmetros:**
- `data_inicio` (date, required): Data inicial do período
- `data_fim` (date, required): Data final do período

**Resposta:**
```json
{
  "vendas": [
    {
      "id": 1,
      "id_venda": "V001",
      "data_venda": "2024-01-01",
      "produto": "Produto A",
      "categoria": "Categoria A",
      "cidade": "São Paulo",
      "quantidade": 10,
      "valor_unitario": 100.00,
      "faturamento": 1000.00
    }
  ]
}
```

### IA

#### Perguntar

Processa uma pergunta em linguagem natural.

```http
POST /api/v1/ia/perguntar
Content-Type: application/json
```

**Body:**
```json
{
  "pergunta": "Qual produto vendeu mais?"
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "pergunta": "Qual produto vendeu mais?",
  "resposta": "O produto mais vendido é Produto A, com 500 unidades vendidas.",
  "sql": "SELECT produto, SUM(quantidade) as total_quantidade FROM vendas GROUP BY produto ORDER BY total_quantidade DESC LIMIT 1;",
  "dados": [
    {
      "produto": "Produto A",
      "total_quantidade": 500
    }
  ]
}
```

## Documentação Interativa

A documentação interativa (Swagger UI) está disponível em:

```
http://localhost:8000/docs
```

A documentação em formato ReDoc está disponível em:

```
http://localhost:8000/redoc
```

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `400 Bad Request`: Requisição inválida
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Erro de validação
- `500 Internal Server Error`: Erro interno do servidor
