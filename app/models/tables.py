from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean
from datetime import datetime
from app.models.database import Base

class SentimentCache(Base):
    __tablename__ = "sentiment_cache"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    label = Column(String)
    score = Column(Float)
    headline_count = Column(Integer)
    low_confidence = Column(Boolean, default=False)
    headlines_json = Column(Text)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    queried_at = Column(DateTime, default=datetime.utcnow)
    result_label = Column(String)