-- Staging model para a tabela de clientes (customers)
with source_customers as (
    select * from {{ source('public', 'customers') }}
)

select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix as zip_code_prefix,
    lower(trim(customer_city)) as city,
    upper(trim(customer_state)) as state
from source_customers
