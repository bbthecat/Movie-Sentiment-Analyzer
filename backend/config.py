from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    OMDB_API_KEY: str | None = Field(default=None)
    TMDB_API_KEY: str | None = Field(default=None)
    HF_MODEL_NAME: str = Field(default="distilbert-base-uncased-finetuned-sst-2-english")
    DATA_DIR: str = Field(default="backend/data")
    TRAKT_CLIENT_ID: str | None = Field(default=None)

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure data dirs exist
base = Path(settings.DATA_DIR)
for sub in ["movies", "reviews", "analysis", "samples"]:
    (base / sub).mkdir(parents=True, exist_ok=True)
