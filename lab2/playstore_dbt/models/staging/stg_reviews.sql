select
    reviewid as review_id,
    app_id,
    score as rating,
    thumbsupcount as thumbs_up_count,
    content as review_text,
    cast("at" as timestamp) as review_timestamp
from {{ ref('reviews_clean') }}
