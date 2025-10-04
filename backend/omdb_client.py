from __future__ import annotations
import requests
from typing import Any, Dict
from .config import settings

BASE_URL = "https://www.omdbapi.com"

class OMDbUnavailable(Exception):
    pass

def _require_key() -> str:
    if not settings.OMDB_API_KEY or settings.OMDB_API_KEY.strip().upper() in {"DUMMY", "YOUR_OMDB_KEY", "YOUR_KEY", "YOURKEY"}:
        raise OMDbUnavailable("OMDb API key missing or dummy; set OMDB_API_KEY in .env")
    return settings.OMDB_API_KEY

def search_movies(query: str) -> Dict[str, Any]:
    key = _require_key()
    resp = requests.get(BASE_URL, params={"s": query, "apikey": key, "type": "movie"}, timeout=15)
    resp.raise_for_status()
    return resp.json()

def get_movie_by_id(imdb_id: str) -> Dict[str, Any]:
    key = _require_key()
    resp = requests.get(BASE_URL, params={"i": imdb_id, "apikey": key, "plot": "short"}, timeout=15)
    resp.raise_for_status()
    return resp.json()
