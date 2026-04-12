from pydantic import BaseModel
from typing import List, Optional

class HeadlineResult(BaseModel):
    headline: str
    score: float
    label: str

class SentimentResponse(BaseModel):
    ticker: str
    label: str
    score: float
    headline_count: int
    low_confidence: bool
    low_confidence_reason: Optional[str]
    cached: bool
    fetched_at: str
    headlines: List[HeadlineResult]