from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import duckdb
import pandas as pd
from langchain_community.llms import Ollama
from langchain_classic.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import json

app = FastAPI(title="Sales Intelligence API")

# Enable CORS for NextJS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MockSQLDatabase:
    dialect = "duckdb"
    @property
    def table_info(self):
        return """
CREATE TABLE fct_sales (deal_id VARCHAR, sales_rep_name VARCHAR, region VARCHAR, industry VARCHAR, amount DOUBLE, expected_revenue DOUBLE, stage VARCHAR, is_won INTEGER, is_lost INTEGER, created_date DATE, close_date DATE);
CREATE TABLE dim_reps (sales_rep_name VARCHAR, total_deals BIGINT, total_won_amount DOUBLE, total_lost_amount DOUBLE, average_win_size DOUBLE, win_rate DOUBLE);
"""
    def get_usable_table_names(self):
        return ["fct_sales", "dim_reps"]
    def get_table_info(self, table_names=None):
        return self.table_info

db = MockSQLDatabase()

# Setup LLM
llm = Ollama(model="phi3:mini")

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Sales Dashboard API is running"}

@app.get("/api/dashboard")
def get_dashboard_summary():
    """Returns static data for the dashboard UI"""
    con = duckdb.connect("../data/warehouse.duckdb", read_only=True)
    
    # Total revenue
    total_rev = con.execute("SELECT SUM(expected_revenue) FROM marts.fct_sales").fetchone()[0]
    
    # Sales by Region
    regions = con.execute("SELECT region, SUM(amount) FROM marts.fct_sales GROUP BY region").fetchall()
    region_data = [{"region": r[0], "amount": r[1]} for r in regions]
    
    # Rep Performance
    reps = con.execute("SELECT sales_rep_name, total_won_amount, total_deals FROM marts.dim_reps ORDER BY total_won_amount DESC LIMIT 5").fetchall()
    rep_data = [{"rep": r[0], "won_amount": r[1], "deals": r[2]} for r in reps]

    con.close()
    
    return {
        "total_revenue": total_rev,
        "sales_by_region": region_data,
        "top_reps": rep_data
    }

@app.post("/api/query")
def text_to_sql_query(request: QueryRequest):
    """Answers plain english questions by querying the warehouse using Langchain"""
    try:
        chain = create_sql_query_chain(llm, db)
        
        # The chain generates a SQL query based on the question
        generated_sql = chain.invoke({"question": request.query})
        
        # Clean the sql string just in case phi3 adds markdown
        cleaned_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        
        # Extract just the SELECT query, discarding any LLM chatter prefix/suffix
        import re
        sql_match = re.search(r"(?i)\b(SELECT\s+.*)", cleaned_sql, re.DOTALL)
        if sql_match:
            cleaned_sql = sql_match.group(1)
            # Remove any trailing conversational text by taking only up to the semicolon
            if ";" in cleaned_sql:
                cleaned_sql = cleaned_sql.split(";")[0]
        
        # Execute query
        con = duckdb.connect("../data/warehouse.duckdb", read_only=True)
        result = con.execute(cleaned_sql).fetchall()
        columns = [desc[0] for desc in con.description]
        con.close()
        
        # Format results into a nice summary using the LLM again
        context = f"Question: {request.query}\nSQL executed: {cleaned_sql}\nData Result: {result}"
        summary_prompt = f"Given this context:\n{context}\nProvide a brief, human-readable answer to the question in under 3 sentences."
        
        human_answer = llm.invoke(summary_prompt)

        return {
            "sql": cleaned_sql,
            "data": [dict(zip(columns, row)) for row in result],
            "answer": human_answer
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
