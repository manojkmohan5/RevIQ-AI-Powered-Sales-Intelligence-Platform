# RevIQ — AI-Powered Sales Intelligence Platform

> Ask your CRM data anything. In plain English.

RevIQ is a full-stack sales analytics platform that combines a local data warehouse, an interactive KPI dashboard, and a conversational AI agent. Powered by LangChain, DuckDB, and a fully local Ollama LLM — no API keys, no cloud dependency.

![Tech Stack](https://img.shields.io/badge/Next.js-black?style=flat&logo=next.js) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=flat&logo=duckdb&logoColor=black) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain) ![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-blueviolet)

---

## What It Does

RevIQ lets anyone — technical or not — explore sales pipeline data through three layers:

- **Live KPI Dashboard** — Total pipeline revenue, win rates, regional breakdowns, and top rep performance, visualized in a modern dark-themed UI.
- **AI Chat Agent** — Type a question like *"Who closed the most deals in APAC?"* and get a plain-English answer, the SQL that was run, and the raw data — all in one shot.
- **Local Data Pipeline** — Mock CRM data is generated, ingested into DuckDB, and modeled with dbt-style transformations entirely on your machine.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TailwindCSS, Recharts, Lucide Icons |
| Backend | FastAPI, LangChain, SQLAlchemy |
| Database | DuckDB (local analytical warehouse) |
| AI / LLM | Ollama `phi3:mini` — fully local inference |
| Data Engineering | Python (Pandas, NumPy), dbt (optional) |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              Next.js Frontend               │
│   Dashboard (Recharts) + AI Chat Interface  │
└────────────────────┬────────────────────────┘
                     │ HTTP (REST)
┌────────────────────▼────────────────────────┐
│              FastAPI Backend                │
│  /api/dashboard  →  DuckDB queries          │
│  /api/query      →  LangChain SQL Chain     │
│                      + Ollama (phi3:mini)   │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│           DuckDB Local Warehouse            │
│   marts.fct_sales  |  marts.dim_reps        │
└─────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running

### 1. Clone the repo

```bash
git clone https://github.com/your-username/reviq.git
cd reviq
```

### 2. Set up the Python backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Build the local data warehouse

```bash
cd scripts
python generate_mock_data.py
python ingest_to_duckdb.py
python run_transformations.py
cd ..
```

### 4. Pull the local LLM

```bash
ollama serve &
ollama pull phi3:mini
```

### 5. Run the full application

```bash
./run.sh
```

> App is live at **http://localhost:3000** — backend runs on port 8000.

---

## Features

### 📊 Analytics Dashboard
- **Total Pipeline Revenue** — aggregated expected revenue across all deals
- **Revenue by Region** — interactive donut chart (NA, EMEA, APAC, LATAM)
- **Top Performing Reps** — horizontal bar chart ranked by closed-won amount

### 🤖 AI Chat Agent
- Natural language → SQL → human-readable answer pipeline
- Powered by LangChain's SQL chain + local `phi3:mini` via Ollama
- Shows the generated SQL in-UI for full transparency
- Example prompts:
  - *"What is our total revenue?"*
  - *"Who is the best sales rep by won amount?"*
  - *"How many deals are in the Negotiation stage?"*

### 🗄️ Data Pipeline
- Generates 2,000 mock CRM deal records across 5 reps, 4 regions, 5 industries, and 6 deal stages
- Ingests raw CSV into a DuckDB warehouse
- Applies transformation models (`fct_sales`, `dim_reps`) for clean analytical layers
- Optional dbt project included under `/dbt_sales`

---

## Project Structure

```
reviq/
├── backend/
│   └── app.py              # FastAPI server + LangChain SQL agent
├── frontend/
│   └── src/app/
│       └── page.tsx        # Dashboard UI + AI chat interface
├── scripts/
│   ├── generate_mock_data.py
│   ├── ingest_to_duckdb.py
│   └── run_transformations.py
├── dbt_sales/
│   └── models/
│       ├── staging/stg_deals.sql
│       └── marts/fct_sales.sql, dim_reps.sql
├── data/                   # Auto-generated DuckDB warehouse
└── run.sh                  # One-command startup script
```

---

## Why Local-First?

RevIQ runs 100% on your machine — no OpenAI key, no cloud database, no external API calls. This makes it a privacy-safe, cost-free demo of production-grade AI analytics patterns that you can run, fork, and extend freely.

---

## License

MIT
