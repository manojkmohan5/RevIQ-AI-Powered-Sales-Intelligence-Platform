import duckdb
import pandas as pd
import os

def ingest_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "raw_crm_data.csv")
    db_path = os.path.join(base_dir, "data", "warehouse.duckdb")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing {csv_path}. Please run generate_mock_data.py first.")
        
    print("Connecting to DuckDB...")
    # Connecting to a file persists the data on disk
    con = duckdb.connect(db_path)
    
    print("Loading CRM data into staging table...")
    # Create schema and table
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    con.execute("DROP TABLE IF EXISTS raw.crm_deals;")
    con.execute(f"CREATE TABLE raw.crm_deals AS SELECT * FROM read_csv_auto('{csv_path}');")
    
    # Verify load
    count = con.execute("SELECT COUNT(*) FROM raw.crm_deals").fetchone()[0]
    print(f"Successfully loaded {count} records into raw.crm_deals!")
    
    con.close()

if __name__ == "__main__":
    ingest_data()
