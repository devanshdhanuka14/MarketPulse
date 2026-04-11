from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.services.ticker_map import get_company_names, is_relevant


app = FastAPI(
    title="MarketPulse API",
    description="Financial news sentiment API for Indian Stocks",
    version="1.0.0"
)

##Pydantic Models
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

@app.get("/health")
def health_check():##just a normal Python function. Name doesn't matter to FastAPI, only the decorator matters.
    return{ ## FastAPI takes whatever dict you return and automatically converts it to a JSON response. 
        "status": "ok",
        "service":"MarketPulse",
        "timestamp": datetime.utcnow().isoformat()
    }

analyzer = SentimentIntensityAnalyzer()

BULLISH_WORDS =["rally", "beats", "upgrade", "surges", "record", "profit", "growth", "buyback", "dividend", "expansion", "buys", "investment", "export", "high", "permits"]
BEARISH_WORDS = ["slump", "miss", "downgrade", "falls", "loss", "weak", "concern", "probe", "debt", "resign", "fraud", "penalty", "fine", "lawsuit", "crash"]

from app.services.news import fetch_news

@app.get("/sentiment/{ticker}", response_model=SentimentResponse)
def get_sentiment(ticker: str):
    headlines, rss_used = fetch_news(ticker)
    
    headlines_list = []
    total_score = 0.0

    for title in headlines:
        vader_dict = analyzer.polarity_scores(title)
        base_score = vader_dict['compound']

        title_lower = title.lower()
        booster = 0.0
        for word in BULLISH_WORDS:
            if word in title_lower:
                booster += 0.10
        for word in BEARISH_WORDS:
            if word in title_lower:
                booster -= 0.10

        final_score = max(-1.0, min(1.0, base_score + booster))

        if final_score >= 0.05:
            label = "Bullish"
        elif final_score <= -0.05:
            label = "Bearish"
        else:
            label = "Neutral"

        total_score += final_score
        headlines_list.append({
            "headline": title,
            "score": round(final_score, 2),
            "label": label
        })

    article_count = len(headlines_list)
    avg_score = round(total_score / article_count, 2) if article_count > 0 else 0.0

    if avg_score >= 0.05:
        overall_label = "Bullish"
    elif avg_score <= -0.05:
        overall_label = "Bearish"
    else:
        overall_label = "Neutral"

    return {
        "ticker": ticker.upper(),
        "label": overall_label,
        "score": avg_score,
        "headline_count": article_count,
        "low_confidence": article_count < 5,
        "low_confidence_reason": "Fewer than 5 relevant headlines found" if article_count < 5 else None,
        "cached": False,
        "fetched_at": datetime.utcnow().isoformat(),
        "headlines": headlines_list
    }