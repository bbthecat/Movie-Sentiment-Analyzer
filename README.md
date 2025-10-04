# Movie Sentiment Analyzer — COMPLETE (Functional + JSON + OMDb + TMDb + HF Sentiment)

A polished FastAPI app that:
- Fetches movie metadata from **OMDb** (public API).
- Imports **user reviews** from **TMDb** (The Movie Database) by IMDb ID.
- Lets you **Upload** CSV/JSON reviews, or **Generate Mock** reviews for demos.
- Runs **Hugging Face sentiment** (with an offline-friendly **fallback**) to classify POS/NEG/NEU.
- Persists everything to **JSON files** and visualizes results in a **beautiful UI** (posters, charts, stats, review cards).

## ✅ Features
- **Public API Integration**: OMDb (metadata), TMDb (reviews import). Optional Trakt (comments) stub ready.
- **Persistence**: JSON under `backend/data/{movies,reviews,analysis}`.
- **Functional Style**: `fetch → analyze → persist → visualize` broken into small modules.
- **CI/CD + Tests**: `pytest`, `flake8`, GitHub Actions, and a local CI script.
- **No network in tests**: tests avoid external calls; sentiment has a fallback.

---

## Quickstart

### 1) Install
```bash
pip install -r requirements.txt
cp .env.sample .env
# Put your keys into .env:
# OMDB_API_KEY=...
# TMDB_API_KEY=...
```

### 2) Run (dev)
```bash
uvicorn backend.app:app --reload
```
Open http://127.0.0.1:8000/

### 3) Docker (optional)
```bash
docker compose up --build
```

---

## .env Settings
```
OMDB_API_KEY=your_omdb_key
TMDB_API_KEY=your_tmdb_key
HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
DATA_DIR=backend/data
# Optional Trakt (not required)
TRAKT_CLIENT_ID=
```

> If `OMDB_API_KEY` missing ⇒ OMDb endpoints are temporarily disabled (cached-only).  
> If `TMDB_API_KEY` missing ⇒ the **Fetch TMDb Reviews** button will fail with a clear error.  
> `HF_MODEL_NAME` can be swapped to another sentiment model if desired.

---

## Endpoints (main)
- `GET /api/health`
- `GET /api/movies/search?query=...`
- `GET /api/movies/{imdb_id}`
- `POST /api/reviews/{imdb_id}/upload` (CSV/JSON)
- `POST /api/reviews/{imdb_id}/use-sample`
- `POST /api/reviews/{imdb_id}/generate?count=40`
- `POST /api/reviews/{imdb_id}/import/tmdb?max_pages=1`
- `POST /api/analyze/{imdb_id}`
- `GET /api/summary/{imdb_id}`
- `GET /api/analysis/{imdb_id}` (detailed rows)
- `GET /api/export/{imdb_id}.csv`
- `POST /api/analyze-text` (single snippet; not persisted)

**Frontend** is available at `/` and calls these endpoints.

---

## Project Structure
```
movie-sentiment-analyzer-complete/
├─ backend/
│  ├─ app.py
│  ├─ config.py
│  ├─ models.py
│  ├─ omdb_client.py
│  ├─ tmdb_client.py
│  ├─ sentiment_hf.py
│  ├─ persistence_json.py
│  └─ data/
│     ├─ movies/
│     ├─ reviews/
│     ├─ analysis/
│     └─ samples/
│        └─ reviews_dune.json
├─ frontend/
│  ├─ index.html
│  ├─ styles.css
│  └─ app.js
├─ tests/
│  ├─ test_analyze.py
│  └─ test_fetch.py
├─ scripts/
│  └─ ci_simulate.sh
├─ .github/workflows/
│  └─ ci.yml
├─ .env.sample
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
```

---

## Notes
- TMDb terms require attribution if used in production; keep usage within TOS.
- This template favors robustness: if the HF model cannot be downloaded, fallback scoring keeps your flows working for demos/tests.
