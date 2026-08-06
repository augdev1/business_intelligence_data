-- Staging model para a tabela de pedidos (orders)
with source_orders as (
    select * from {{ source('public', 'orders') }}
)

select
    order_id,
    customer_id,
    lower(trim(order_status)) as order_status,
    cast(order_purchase_timestamp as timestamp) as purchase_timestamp,
    cast(order_approved_at as timestamp) as approved_at,
    cast(order_delivered_carrier_date as timestamp) as delivered_carrier_date,
    cast(order_delivered_customer_date as timestamp) as delivered_customer_date,
    cast(order_estimated_delivery_date as timestamp) as estimated_delivery_date
from source_orders
