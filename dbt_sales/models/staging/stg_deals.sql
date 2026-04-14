WITH source AS (
    SELECT * FROM raw.crm_deals
)

SELECT
    deal_id,
    sales_rep_name,
    region,
    company_name,
    industry,
    CAST(amount AS DOUBLE) AS amount,
    stage,
    CAST(probability AS DOUBLE) AS probability,
    CAST(created_date AS DATE) AS created_date,
    CAST(close_date AS DATE) AS close_date,
    CAST(amount * probability AS DOUBLE) AS expected_revenue
FROM source
