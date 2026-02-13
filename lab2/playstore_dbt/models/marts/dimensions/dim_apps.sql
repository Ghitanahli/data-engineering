with apps as (

    select *
    from {{ ref('stg_apps') }}

),

developers as (

    select *
    from {{ ref('dim_developers') }}

),

categories as (

    select *
    from {{ ref('dim_categories') }}

)

select
    row_number() over (order by a.app_id) as app_key,
    a.app_id,
    a.app_name,
    d.developer_key,
    c.category_key,
    a.price,
    a.is_paid,
    a.installs,
    a.catalog_rating,
    a.ratings_count
from apps a
left join developers d
    on a.developer_name = d.developer_name
left join categories c
    on a.category_name = c.category_name
