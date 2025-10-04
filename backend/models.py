from pydantic import BaseModel, Field
from typing import Optional, List

class Review(BaseModel):
    text: str
    source: Optional[str] = None
    timestamp: Optional[str] = None

class SentimentResult(BaseModel):
    label: str
    score: float
    text: str
    source: Optional[str] = None
    timestamp: Optional[str] = None

class SummaryResponse(BaseModel):
    imdb_id: str
    total: int
    positives: int
    negatives: int
    neutral: int
    positivity_ratio: float
    avg_confidence: float
    top_positive_quotes: list[str]
    top_negative_quotes: list[str]
