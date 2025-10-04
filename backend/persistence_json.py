from __future__ import annotations
import json
from pathlib import Path
from typing import Any, List, Dict
from .config import settings

BASE = Path(settings.DATA_DIR)

def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def movie_path(imdb_id: str) -> Path:
    return BASE / "movies" / f"{imdb_id}.json"

def reviews_path(imdb_id: str) -> Path:
    return BASE / "reviews" / f"{imdb_id}_raw.json"

def analysis_path(imdb_id: str) -> Path:
    return BASE / "analysis" / f"{imdb_id}_sentiment.json"

def save_movie_meta(imdb_id: str, meta: Dict[str, Any]) -> None:
    _write_json(movie_path(imdb_id), meta)

def load_movie_meta(imdb_id: str) -> Dict[str, Any] | None:
    return _read_json(movie_path(imdb_id))

def save_reviews(imdb_id: str, reviews: List[Dict[str, Any]]) -> None:
    _write_json(reviews_path(imdb_id), reviews)

def load_reviews(imdb_id: str) -> List[Dict[str, Any]] | None:
    return _read_json(reviews_path(imdb_id))

def save_analysis(imdb_id: str, rows: List[Dict[str, Any]]) -> None:
    _write_json(analysis_path(imdb_id), rows)

def load_analysis(imdb_id: str) -> List[Dict[str, Any]] | None:
    return _read_json(analysis_path(imdb_id))
