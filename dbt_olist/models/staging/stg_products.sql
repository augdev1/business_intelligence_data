-- Staging model para a tabela de produtos (products)
with source_products as (
    select * from {{ source('public', 'products') }}
)

select
    product_id,
    coalesce(lower(trim(product_category_name)), 'nao_definido') as category_name,
    cast(product_name_lenght as integer) as name_length,
    cast(product_description_lenght as integer) as description_length,
    cast(product_photos_qty as integer) as photos_qty,
    cast(product_weight_g as numeric(10,2)) as weight_g,
    cast(product_length_cm as numeric(10,2)) as length_cm,
    cast(product_height_cm as numeric(10,2)) as height_cm,
    cast(product_width_cm as numeric(10,2)) as width_cm
from source_products
