from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import csv, io, os, json, datetime

# Import backend modules
from backend.config import settings
from backend import omdb_client
from backend import tmdb_client
from backend.persistence_json import (
    save_movie_meta, load_movie_meta,
    save_reviews, load_reviews,
    save_analysis, load_analysis,
)
from backend.models import SummaryResponse
from backend.sentiment_hf import predict as hf_predict

app = FastAPI(
    title="Movie Sentiment Analyzer",
    description="AI-powered movie sentiment analysis",
    version="1.0.0"
)

# Add permissive CORS (Render default is fine with this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Health check endpoint
@app.get("/api/health")
def health():
    return {"ok": True, "status": "healthy", "platform": "render", "version": "1.0.0"}

# Root endpoint - serve frontend
@app.get("/", response_class=HTMLResponse)
def root():
    html_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="""
        <html>
            <head><title>Movie Sentiment Analyzer</title></head>
            <body>
                <h1>🎬 Movie Sentiment Analyzer</h1>
                <p>API is running! Frontend files not found.</p>
                <p><a href="/docs">API Documentation</a></p>
                <p><a href="/api/health">Health Check</a></p>
            </body>
        </html>
        """)

# -------- Movies (OMDb) --------
@app.get("/api/movies/search")
def movie_search(query: str):
    try:
        data = omdb_client.search_movies(query)
        return data
    except omdb_client.OMDbUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/api/movies/{imdb_id}")
def movie_get(imdb_id: str):
    try:
        data = omdb_client.get_movie_by_id(imdb_id)
        if data.get("Response") == "True":
            save_movie_meta(imdb_id, data)
        return data
    except omdb_client.OMDbUnavailable as e:
        cached = load_movie_meta(imdb_id)
        if cached:
            return cached
        raise HTTPException(status_code=503, detail=str(e))

# -------- Reviews: upload / sample / generate --------
@app.post("/api/reviews/{imdb_id}/upload")
async def reviews_upload(imdb_id: str, file: UploadFile | None = File(default=None)):
    texts: List[Dict[str, Any]] = []
    if file is None:
        raise HTTPException(400, "Please upload a CSV or JSON file, or use /use-sample")

    content = await file.read()
    name = (file.filename or "").lower()
    try:
        if name.endswith(".csv"):
            s = content.decode("utf-8", errors="ignore")
            reader = csv.DictReader(io.StringIO(s))
            for row in reader:
                texts.append({"text": row.get("text",""), "source": row.get("source"), "timestamp": row.get("timestamp")})
        else:
            data = json.loads(content.decode("utf-8", errors="ignore"))
            if isinstance(data, list):
                for r in data:
                    texts.append({
                        "text": r.get("text",""),
                        "source": r.get("source"),
                        "timestamp": r.get("timestamp")
                    })
            else:
                raise ValueError("JSON must be a list of review objects")
    except Exception as e:
        raise HTTPException(400, f"Failed to parse file: {e}")

    texts = [t for t in texts if t.get("text")]
    if not texts:
        raise HTTPException(400, "No valid reviews found")
    save_reviews(imdb_id, texts)
    return {"ok": True, "count": len(texts)}

@app.post("/api/reviews/{imdb_id}/use-sample")
def reviews_use_sample(imdb_id: str):
    sample_path = os.path.join(settings.DATA_DIR, "samples", "reviews_dune.json")
    if not os.path.exists(sample_path):
        raise HTTPException(400, "Sample not available")
    texts = json.loads(open(sample_path, "r", encoding="utf-8").read())
    save_reviews(imdb_id, texts)
    return {"ok": True, "count": len(texts), "note": "used sample"}

@app.post("/api/reviews/{imdb_id}/generate")
def reviews_generate(imdb_id: str, count: int = 40):
    pos_templates = [
        "Amazing movie with stunning visuals!",
        "Great acting and beautiful score.",
        "Loved it, a must watch.",
        "Fantastic world-building and direction.",
        "I enjoyed every minute!"
    ]
    neg_templates = [
        "Boring and too slow.",
        "I hate the pacing, overhyped.",
        "Terrible writing and confusing plot.",
        "Awful experience, not worth it.",
        "Disappointing and dull."
    ]
    neu_templates = [
        "It was okay, nothing special.",
        "Fine movie with some good moments.",
        "Average overall.",
        "Mixed feelings about it.",
        "Neutral on this one."
    ]

    import random
    rows: List[Dict[str, Any]] = []
    n_pos = max(1, int(count * 0.4))
    n_neg = max(1, int(count * 0.3))
    n_neu = max(1, count - n_pos - n_neg)

    def mk(templates, n):
        out = []
        for _ in range(n):
            t = random.choice(templates)
            ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
            out.append({"text": t, "source": "mock", "timestamp": ts})
        return out

    rows.extend(mk(pos_templates, n_pos))
    rows.extend(mk(neg_templates, n_neg))
    rows.extend(mk(neu_templates, n_neu))

    save_reviews(imdb_id, rows)
    return {"ok": True, "count": len(rows), "note": "mock reviews generated"}

# -------- Reviews: add single comment --------
@app.post("/api/reviews/{imdb_id}/add")
def reviews_add(imdb_id: str, payload: dict):
    text = (payload or {}).get("text", "").strip()
    source = (payload or {}).get("source")
    if not text:
        raise HTTPException(400, "Missing 'text'")

    existing = load_reviews(imdb_id) or []
    ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    new_item = {"text": text, "source": source or "user", "timestamp": ts}
    # append and persist full list
    existing.append(new_item)
    save_reviews(imdb_id, existing)
    return {"ok": True, "count": len(existing), "added": new_item}

# -------- Reviews: import from TMDb --------
@app.post("/api/reviews/{imdb_id}/import/tmdb")
def reviews_import_tmdb(imdb_id: str, max_pages: int = 1):
    try:
        tmdb_id = tmdb_client.find_tmdb_id_by_imdb(imdb_id)
        if not tmdb_id:
            return {"ok": False, "count": 0, "msg": "Not found on TMDb"}
        rows: List[Dict[str, Any]] = []
        for page in range(1, max_pages + 1):
            for r in tmdb_client.fetch_reviews_by_tmdb_id(tmdb_id, page=page):
                rows.append({
                    "text": r.get("content",""),
                    "source": f"tmdb:{r.get('author','')}",
                    "timestamp": r.get("created_at")
                })
        if not rows:
            return {"ok": True, "count": 0, "msg": "No reviews on TMDb"}
        # Merge TMDb reviews into existing instead of overwriting
        existing = load_reviews(imdb_id) or []
        merged = existing + rows
        save_reviews(imdb_id, merged)
        return {"ok": True, "count": len(rows), "total": len(merged)}
    except tmdb_client.TMDbUnavailable as e:
        raise HTTPException(503, str(e))
    except Exception as e:
        raise HTTPException(500, f"TMDb import failed: {e}")

# -------- Analyze / Summary --------
@app.post("/api/analyze/{imdb_id}")
def analyze(imdb_id: str):
    reviews = load_reviews(imdb_id)
    if not reviews:
        raise HTTPException(404, "No reviews uploaded/imported for this movie")

    texts = [r.get("text","") for r in reviews]
    preds = hf_predict(texts)

    rows: List[Dict[str, Any]] = []
    for r, p in zip(reviews, preds):
        rows.append({
            "text": r.get("text",""),
            "source": r.get("source"),
            "timestamp": r.get("timestamp"),
            "label": p["label"],
            "score": float(p["score"]),
        })
    save_analysis(imdb_id, rows)
    return {"ok": True, "count": len(rows)}

@app.get("/api/summary/{imdb_id}", response_model=SummaryResponse)
def summary(imdb_id: str):
    rows = load_analysis(imdb_id)
    if not rows:
        raise HTTPException(404, "No analysis found; run /api/analyze first")

    total = len(rows)
    pos = sum(1 for r in rows if r["label"].upper().startswith("POS"))
    neg = sum(1 for r in rows if r["label"].upper().startswith("NEG"))
    neu = total - pos - neg
    avg = sum(r.get("score", 0.0) for r in rows) / total if total else 0.0

    top_pos = sorted([r for r in rows if r["label"].upper().startswith("POS")], key=lambda x: x.get("score",0), reverse=True)[:5]
    top_neg = sorted([r for r in rows if r["label"].upper().startswith("NEG")], key=lambda x: x.get("score",0), reverse=True)[:5]

    return {
        "imdb_id": imdb_id,
        "total": total,
        "positives": pos,
        "negatives": neg,
        "neutral": neu,
        "positivity_ratio": round(pos/total, 4) if total else 0.0,
        "avg_confidence": round(avg, 4),
        "top_positive_quotes": [t["text"] for t in top_pos],
        "top_negative_quotes": [t["text"] for t in top_neg],
    }

@app.get("/api/analysis/{imdb_id}")
def get_analysis(imdb_id: str):
    rows = load_analysis(imdb_id)
    if not rows:
        raise HTTPException(404, "No analysis found; run /api/analyze first")
    return {"imdb_id": imdb_id, "rows": rows}

# Raw reviews (no labels) - helpful to fetch user-added comments directly
@app.get("/api/reviews/{imdb_id}")
def get_reviews_raw(imdb_id: str):
    reviews = load_reviews(imdb_id) or []
    return {"imdb_id": imdb_id, "count": len(reviews), "reviews": reviews}

@app.get("/api/export/{imdb_id}.csv")
def export_csv(imdb_id: str):
    rows = load_analysis(imdb_id)
    if not rows:
        raise HTTPException(404, "No analysis to export")

    fieldnames = ["text","source","timestamp","label","score"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r.get(k,"") for k in fieldnames})

    data = buf.getvalue().encode("utf-8")
    return Response(
        content=data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{imdb_id}_analysis.csv"'
        }
    )

# Single text analysis (no persistence)
@app.post("/api/analyze-text")
def analyze_text(payload: dict):
    text = payload.get("text", "")
    if not text.strip():
        raise HTTPException(400, "Missing 'text'")
    pred = hf_predict([text])[0]
    return {"label": pred["label"], "score": pred["score"]}

# Cleaned up for Render: no serverless adapter needed
