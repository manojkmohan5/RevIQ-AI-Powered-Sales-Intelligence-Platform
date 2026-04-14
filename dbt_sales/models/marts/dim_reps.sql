WITH stg_deals AS (
    SELECT * FROM {{ ref('stg_deals') }}
)

SELECT
    sales_rep_name,
    COUNT(deal_id) AS total_deals,
    SUM(CASE WHEN stage = 'Closed Won' THEN amount ELSE 0 END) AS total_won_amount,
    SUM(CASE WHEN stage = 'Closed Lost' THEN amount ELSE 0 END) AS total_lost_amount,
    AVG(CASE WHEN stage = 'Closed Won' THEN amount ELSE NULL END) AS average_win_size,
    COUNT(CASE WHEN stage = 'Closed Won' THEN 1 END) * 1.0 / NULLIF(COUNT(deal_id), 0) AS win_rate
FROM stg_deals
GROUP BY 1
