select
    row_number() over (order by developer_name) as developer_key,
    developer_name,
    null as developer_website,
    null as developer_email
from (
    select distinct developer_name
    from {{ ref('stg_apps') }}
)
