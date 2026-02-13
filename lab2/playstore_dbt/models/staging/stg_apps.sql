select
    appid as app_id,
    title as app_name,
    developer as developer_name,
    genre as category_name,
    price,
    case when price > 0 then true else false end as is_paid,
    installs,
    score as catalog_rating,
    ratings as ratings_count
from {{ ref('apps_catalog') }}
