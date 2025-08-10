# JobFinder: Vector & Keyword Search for Job Postings

A modern, end-to-end demo for job search using Weaviate vector database, FastAPI, and Streamlit. Supports exact (BM25), semantic, and hybrid search across all job fields.

---

## Features
- **Weaviate Vector DB**: Store and search job postings with both vector and keyword (BM25) search
- **FastAPI Backend**: Exposes endpoints for exact, semantic, and hybrid search
- **Streamlit UI**: User-friendly web interface for searching jobs
- **Batch Ingestion**: Load jobs from CSV into Weaviate
- **Flexible Filtering**: Search by any combination of job fields

---

## Project Structure

```
JobFinder/
├── clean_job_data.py                # Data cleaning script
├── create_weaviate_schema.py        # Weaviate schema creation
├── docker-compose.yml               # (Optional) For running Weaviate locally
├── ingest_job_data.py               # Ingest jobs from CSV to Weaviate
├── job_dataset_demo.csv             # Demo job dataset
├── job_descriptions.csv             # Additional job descriptions
├── job_search_api.py                # FastAPI backend
├── load_job_dataset_to_weaviate.py  # Alternative ingestion script
├── requirements_streamlit.txt       # Streamlit UI dependencies
├── requirements_weaviate.txt        # Weaviate/Backend dependencies
├── streamlit_app.py                 # Streamlit UI
└── ... (other docs, scripts)
```

---

## Quickstart

### 1. Install Weaviate (if not using cloud)
- Use Docker Compose or follow [Weaviate docs](https://weaviate.io/developers/weaviate/installation)

```
docker-compose up -d
```

### 2. Install Python dependencies

- Backend (Weaviate, FastAPI):
  ```bash
  pip install -r requirements_weaviate.txt
  ```
- UI (Streamlit):
  ```bash
  pip install -r requirements_streamlit.txt
  ```

### 3. Create Weaviate schema

```bash
python create_weaviate_schema.py
```

### 4. Ingest job data

```bash
python ingest_job_data.py
```

### 5. Start FastAPI backend

```bash
uvicorn job_search_api:app --reload
```

### 6. Start Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

## API Endpoints (FastAPI)

- `GET /jobs/all?offset=0&limit=10` — Paginated list of all jobs
- `GET /search/exact?...` — BM25/keyword search (all fields supported)
- `POST /search/semantic` — Semantic/vector search
- `POST /search/hybrid` — Hybrid (BM25 + vector) search

See code for full parameter details.

---

## Streamlit UI
- Choose search type: All, Exact, Semantic, Hybrid
- Search by any combination of job fields
- Paginated results, expandable job cards
- See scores/distances for ranking

---

## Customization
- Update schema or ingestion scripts for your own job data
- Extend FastAPI endpoints for more advanced filters
- Tweak Streamlit UI for your workflow

---

## Troubleshooting
- Make sure Weaviate is running and accessible
- Ensure FastAPI and Streamlit are running on the correct ports (default: 8000, 8501)
- Check requirements files for missing dependencies

---

## Credits
- Built with [Weaviate](https://weaviate.io/), [FastAPI](https://fastapi.tiangolo.com/), [Streamlit](https://streamlit.io/)

---

