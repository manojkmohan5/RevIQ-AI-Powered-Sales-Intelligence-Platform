WITH stg_deals AS (
    SELECT * FROM {{ ref('stg_deals') }}
)

SELECT
    deal_id,
    sales_rep_name,
    region,
    industry,
    amount,
    expected_revenue,
    stage,
    CASE WHEN stage = 'Closed Won' THEN 1 ELSE 0 END AS is_won,
    CASE WHEN stage = 'Closed Lost' THEN 1 ELSE 0 END AS is_lost,
    created_date,
    close_date
FROM stg_deals
