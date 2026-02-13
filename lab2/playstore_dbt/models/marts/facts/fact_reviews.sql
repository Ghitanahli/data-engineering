{{ config(
    materialized='incremental',
    unique_key='review_id'
) }}
with reviews as (

    select *
    from {{ ref('stg_reviews') }}

    {% if is_incremental() %}
        where review_id not in (select review_id from {{ this }})
    {% endif %}

),

apps as (

    select *
    from {{ ref('dim_apps') }}

)

select
    r.review_id,
    a.app_key,
    a.developer_key,
    cast(strftime('%Y%m%d', r.review_timestamp) as integer) as date_key,
    r.rating,
    r.thumbs_up_count,
    r.review_text,
    null as review_version
from reviews r
left join apps a
    on r.app_id = a.app_id
where a.app_key is not null

