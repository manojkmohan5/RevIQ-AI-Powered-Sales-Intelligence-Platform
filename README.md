# Nexus Intelligence Pipeline

A modern, end-to-end sales intelligence and data analytics platform. This application integrates a full data pipeline with an interactive frontend dashboard and an AI-powered conversational interface for interacting with and querying the data in plain English.

## Tech Stack
- **Frontend**: Next.js (React), TailwindCSS, Recharts
- **Backend**: FastAPI (Python), LangChain, DuckDB, Ollama
- **Data Engineering**: Data generated via Python scripts and ingested into a local DuckDB warehouse

## Features
- **Interactive Dashboard**: View complete pipeline revenue, win rates, and rep performances via a modern UI.
- **AI Chat Agent**: Ask your data questions directly in plain English. Powered by LangChain and a localized Ollama instance (`phi3:mini` model) to execute DuckDB analytical queries dynamically.
- **Local Data Warehouse**: Utilizes DuckDB for high-performant localized analytical processing.

## Getting Started

1. Set up a Python virtual environment and install backend dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt # if available
   ```

2. Initialize the internal DuckDB Data Warehouse:
   ```bash
   cd scripts
   python generate_mock_data.py
   python ingest_to_duckdb.py
   python run_transformations.py
   cd ..
   ```

3. Ensure Ollama is running optimally and verify context models:
   ```bash
   ollama serve &
   ollama pull phi3:mini
   ```

4. Run the complete application (both Backend & Frontend):
   ```bash
   ./run.sh
   ```
   > The application will be live at `http://localhost:3000`.

## Architecture Details
- `/frontend` - Next.js UI using `recharts` for charts.
- `/backend` - FastAPI server utilizing LangChain's SQL chains to generate and execute dynamic queries.
- `/scripts` - Database population sequence utilizing Pandas and DuckDB connections.
- `/dbt_sales` - dbt pipeline setups (optional expansion).
