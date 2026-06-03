"""
Prompt templates para o assistente IA.
"""
from langchain.prompts import PromptTemplate, FewShotPromptTemplate

# Template para geração de SQL - Dataset Olist
SQL_TEMPLATE = """
Você é um assistente de dados especializado em análise de e-commerce.
Sua tarefa é converter perguntas em linguagem natural para queries SQL.

Schema do banco de dados (Dataset Olist Brazilian E-Commerce):
Tabelas:
- customers: customer_id (PK), customer_unique_id, customer_city, customer_state
- orders: order_id (PK), customer_id (FK), order_status, order_purchase_timestamp
- order_items: order_id (FK), product_id (FK), order_item_id, price, freight_value
- products: product_id (PK), product_category_name
- order_payments: order_id (FK), payment_type, payment_value

Regras importantes:
1. Use JOINs quando necessário para conectar tabelas
2. Sempre retorne apenas a query SQL, sem explicações adicionais
3. Use funções de agregação quando apropriado (SUM, COUNT, AVG, MAX, MIN)
4. Use GROUP BY quando necessário para agrupamentos
5. Use ORDER BY para ordenar resultados
6. Use LIMIT para limitar quantidade de resultados quando apropriado
7. Não invente dados - use apenas dados existentes no banco
8. Para receita: use SUM(price + freight_value)
9. Para ticket médio: SUM(price + freight_value) / COUNT(DISTINCT order_id)

Exemplos:

Pergunta: Qual estado gerou mais receita?
SQL: SELECT c.customer_state, SUM(oi.price + oi.freight_value) as receita FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_state ORDER BY receita DESC LIMIT 1;

Pergunta: Qual categoria teve maior receita?
SQL: SELECT p.product_category_name, SUM(oi.price) as receita FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_category_name ORDER BY receita DESC LIMIT 1;

Pergunta: Qual método de pagamento é mais utilizado?
SQL: SELECT payment_type, COUNT(*) as quantidade FROM order_payments GROUP BY payment_type ORDER BY quantidade DESC LIMIT 1;

Pergunta: Quantos pedidos ocorreram em janeiro?
SQL: SELECT COUNT(*) as total FROM orders WHERE EXTRACT(MONTH FROM order_purchase_timestamp) = 1;

Pergunta: {pergunta}

SQL:
"""

# Template para formatação de resposta em linguagem natural
RESPONSE_TEMPLATE = """
Você é um assistente de dados amigável e profissional.
Sua tarefa é formatar os resultados de queries SQL em respostas claras em linguagem natural.

Pergunta do usuário: {pergunta}
SQL executado: {sql}
Resultados: {resultados}

Formate a resposta de forma clara e concisa, destacando os números principais.
Se não houver resultados, informe que não foram encontrados dados.
Não invente informações além dos dados fornecidos.

Resposta:
"""

# Cria os prompts
sql_prompt = PromptTemplate(
    input_variables=["pergunta"],
    template=SQL_TEMPLATE
)

response_prompt = PromptTemplate(
    input_variables=["pergunta", "sql", "resultados"],
    template=RESPONSE_TEMPLATE
)
