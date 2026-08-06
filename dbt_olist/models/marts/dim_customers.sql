-- Dimensão de Clientes (dim_customers) - Camada Marts/Gold
with customers as (
    select * from {{ ref('stg_customers') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
),
customer_orders_summary as (
    select
        customer_id,
        count(distinct order_id) as total_orders,
        min(purchase_timestamp) as first_order_at,
        max(purchase_timestamp) as last_order_at
    from orders
    group by customer_id
)

select
    c.customer_id,
    c.customer_unique_id,
    c.zip_code_prefix,
    c.city,
    c.state,
    coalesce(s.total_orders, 0) as total_orders,
    s.first_order_at,
    s.last_order_at
from customers c
left join customer_orders_summary s on c.customer_id = s.customer_id
