import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.tables import SentimentCache, SearchHistory

CACHE_TTL_MINUTES = 30

def get_cached_result(ticker: str, db: Session):
    cutoff = datetime.utcnow() - timedelta(minutes=CACHE_TTL_MINUTES)
    result = db.query(SentimentCache)\
        .filter(SentimentCache.ticker == ticker.upper())\
        .filter(SentimentCache.fetched_at >= cutoff)\
        .order_by(SentimentCache.fetched_at.desc())\
        .first()
    return result

def store_result(ticker: str, label: str, score: float,
                 headline_count: int, low_confidence: bool,
                 headlines: list, db: Session):
    record = SentimentCache(
        ticker=ticker.upper(),
        label=label,
        score=score,
        headline_count=headline_count,
        low_confidence=low_confidence,
        headlines_json=json.dumps(headlines),
        fetched_at=datetime.utcnow()
    )
    db.add(record)
    db.commit()

def log_search(ticker: str, label: str, db: Session):
    record = SearchHistory(
        ticker=ticker.upper(),
        queried_at=datetime.utcnow(),
        result_label=label
    )
    db.add(record)
    db.commit()