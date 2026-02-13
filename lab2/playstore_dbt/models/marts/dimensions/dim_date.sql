select distinct
    cast(strftime('%Y%m%d', review_timestamp) as integer) as date_key,
    cast(review_timestamp as date) as date,
    extract(year from review_timestamp) as year,
    extract(month from review_timestamp) as month,
    extract(quarter from review_timestamp) as quarter,
    extract(dow from review_timestamp) as day_of_week,
    case 
        when extract(dow from review_timestamp) in (0,6) then true
        else false
    end as is_weekend
from {{ ref('stg_reviews') }}
