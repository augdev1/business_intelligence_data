-- Dimensão de Produtos (dim_products) - Camada Marts/Gold
with products as (
    select * from {{ ref('stg_products') }}
),
order_items as (
    select * from {{ ref('stg_order_items') }}
),
product_sales_summary as (
    select
        product_id,
        count(distinct order_id) as total_orders_count,
        count(*) as total_items_sold,
        sum(price) as total_revenue_generated
    from order_items
    group by product_id
)

select
    p.product_id,
    p.category_name,
    p.name_length,
    p.description_length,
    p.photos_qty,
    p.weight_g,
    p.length_cm,
    p.height_cm,
    p.width_cm,
    coalesce(s.total_items_sold, 0) as total_items_sold,
    coalesce(s.total_revenue_generated, 0.00) as total_revenue_generated
from products p
left join product_sales_summary s on p.product_id = s.product_id
