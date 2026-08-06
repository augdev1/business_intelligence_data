-- Staging model para a tabela de pagamentos dos pedidos (order_payments)
with source_order_payments as (
    select * from {{ source('public', 'order_payments') }}
)

select
    order_id,
    cast(payment_sequential as integer) as payment_sequential,
    lower(trim(payment_type)) as payment_type,
    cast(payment_installments as integer) as payment_installments,
    cast(payment_value as numeric(10,2)) as payment_value
from source_order_payments
