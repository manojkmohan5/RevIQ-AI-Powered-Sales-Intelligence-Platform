import duckdb

def run_transformations():
    print("Connecting to DuckDB Warehouse...")
    import os
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "warehouse.duckdb")
    con = duckdb.connect(db_path)
    
    print("Creating Staging Views...")
    con.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    con.execute("DROP VIEW IF EXISTS staging.stg_deals;")
    con.execute("""
        CREATE VIEW staging.stg_deals AS 
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
        FROM raw.crm_deals
    """)
    
    print("Creating Mart Tables...")
    con.execute("CREATE SCHEMA IF NOT EXISTS marts;")
    con.execute("DROP TABLE IF EXISTS marts.fct_sales;")
    con.execute("""
        CREATE TABLE marts.fct_sales AS 
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
        FROM staging.stg_deals
    """)
    
    con.execute("DROP TABLE IF EXISTS marts.dim_reps;")
    con.execute("""
        CREATE TABLE marts.dim_reps AS 
        SELECT
            sales_rep_name,
            COUNT(deal_id) AS total_deals,
            SUM(CASE WHEN stage = 'Closed Won' THEN amount ELSE 0 END) AS total_won_amount,
            SUM(CASE WHEN stage = 'Closed Lost' THEN amount ELSE 0 END) AS total_lost_amount,
            AVG(CASE WHEN stage = 'Closed Won' THEN amount ELSE NULL END) AS average_win_size,
            COUNT(CASE WHEN stage = 'Closed Won' THEN 1 END) * 1.0 / NULLIF(COUNT(deal_id), 0) AS win_rate
        FROM staging.stg_deals
        GROUP BY 1
    """)
    
    # Verify counts
    fct_count = con.execute("SELECT COUNT(*) FROM marts.fct_sales").fetchone()[0]
    dim_count = con.execute("SELECT COUNT(*) FROM marts.dim_reps").fetchone()[0]
    
    print(f"Transformations successful! Created fct_sales ({fct_count}) and dim_reps ({dim_count}).")
    con.close()

if __name__ == "__main__":
    run_transformations()
