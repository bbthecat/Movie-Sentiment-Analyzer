from __future__ import annotations
import requests
from typing import Any, Dict, List
from .config import settings

TMDB_BASE = "https://api.themoviedb.org/3"

class TMDbUnavailable(Exception):
    pass

def _require_key() -> str:
    if not settings.TMDB_API_KEY or settings.TMDB_API_KEY.strip().upper() in {"DUMMY", "YOUR_TMDB_KEY", "YOUR_KEY", "YOURKEY"}:
        raise TMDbUnavailable("TMDb API key missing or dummy; set TMDB_API_KEY in .env")
    return settings.TMDB_API_KEY

def find_tmdb_id_by_imdb(imdb_id: str) -> int | None:
    key = _require_key()
    try:
        r = requests.get(f"{TMDB_BASE}/find/{imdb_id}", params={"api_key": key, "external_source": "imdb_id"}, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("movie_results") or []
        return results[0]["id"] if results else None
    except requests.exceptions.RequestException as e:
        raise TMDbUnavailable(f"TMDb API error: {str(e)}")
    except (KeyError, IndexError, ValueError) as e:
        raise TMDbUnavailable(f"TMDb API returned unexpected data: {str(e)}")

def fetch_reviews_by_tmdb_id(tmdb_id: int, page: int = 1) -> List[Dict[str, Any]]:
    key = _require_key()
    try:
        r = requests.get(f"{TMDB_BASE}/movie/{tmdb_id}/reviews", params={"api_key": key, "page": page}, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        raise TMDbUnavailable(f"TMDb API error: {str(e)}")
    except (KeyError, ValueError) as e:
        raise TMDbUnavailable(f"TMDb API returned unexpected data: {str(e)}")
