{% snapshot snapshot_dim_apps %}

{{
    config(
      target_schema='main',
      unique_key='app_id',
      strategy='check',
      check_cols=['app_name','price','installs','catalog_rating']
    )
}}

select *
from {{ ref('stg_apps') }}

{% endsnapshot %}
