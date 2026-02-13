select
    row_number() over (order by category_name) as category_key,
    category_name
from (
    select distinct category_name
    from {{ ref('stg_apps') }}
)
