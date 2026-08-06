-- Tabela Fato de Pedidos (fct_orders) - Camada Marts/Gold
with orders as (
    select * from {{ ref('stg_orders') }}
),
order_items as (
    select
        order_id,
        count(distinct item_id_composite) as total_items,
        sum(price) as total_price,
        sum(freight_value) as total_freight
    from (
        select order_id, order_item_id as item_id_composite, price, freight_value 
        from {{ ref('stg_order_items') }}
    ) sub
    group by order_id
),
order_payments as (
    select
        order_id,
        sum(payment_value) as total_payment_value,
        max(payment_installments) as max_installments,
        min(payment_type) as primary_payment_type
    from {{ ref('stg_order_payments') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_timestamp,
    o.approved_at,
    o.delivered_carrier_date,
    o.delivered_customer_date,
    o.estimated_delivery_date,
    coalesce(i.total_items, 0) as total_items,
    coalesce(i.total_price, 0.00) as total_items_price,
    coalesce(i.total_freight, 0.00) as total_freight_value,
    (coalesce(i.total_price, 0.00) + coalesce(i.total_freight, 0.00)) as total_order_value,
    coalesce(p.total_payment_value, 0.00) as total_payment_value,
    coalesce(p.max_installments, 0) as max_installments,
    coalesce(p.primary_payment_type, 'nao_informado') as primary_payment_type
from orders o
left join order_items i on o.order_id = i.order_id
left join order_payments p on o.order_id = p.order_id
