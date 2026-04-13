import json
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.news import fetch_news
from app.services.sentiment import score_headlines
from app.services.cache import get_cached_result, store_result, log_search
from app.models.schemas import SentimentResponse

router = APIRouter()

@router.get("/sentiment/{ticker}", response_model=SentimentResponse)
def get_sentiment(ticker: str, db: Session = Depends(get_db)):

    if "." not in ticker:
        ticker = ticker + ".NS"
    ticker = ticker.upper()
    
    cached = get_cached_result(ticker, db)
    if cached:
        log_search(ticker, cached.label, db)
        return {
            "ticker": cached.ticker,
            "label": cached.label,
            "score": cached.score,
            "headline_count": cached.headline_count,
            "low_confidence": cached.low_confidence,
            "low_confidence_reason": "Fewer than 5 relevant headlines found" if cached.low_confidence else None,
            "cached": True,
            "fetched_at": cached.fetched_at.isoformat(),
            "headlines": json.loads(cached.headlines_json)
        }

    headlines, rss_used = fetch_news(ticker)
    headlines_list, avg_score, overall_label = score_headlines(headlines)

    article_count = len(headlines_list)
    low_confidence = article_count < 5

    store_result(ticker, overall_label, avg_score, article_count,
                 low_confidence, headlines_list, db)
    log_search(ticker, overall_label, db)

    return {
        "ticker": ticker.upper(),
        "label": overall_label,
        "score": avg_score,
        "headline_count": article_count,
        "low_confidence": low_confidence,
        "low_confidence_reason": "Fewer than 5 relevant headlines found" if low_confidence else None,
        "cached": False,
        "fetched_at": datetime.utcnow().isoformat(),
        "headlines": headlines_list
    }