from fastapi import FastAPI
from datetime import datetime
from app.models.database import engine
from app.models import tables
from app.routes import sentiment, history

tables.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MarketPulse API",
    description="Financial news sentiment API for Indian stocks",
    version="1.0.0"
)

app.include_router(sentiment.router)
app.include_router(history.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MarketPulse",
        "timestamp": datetime.utcnow().isoformat()
    }