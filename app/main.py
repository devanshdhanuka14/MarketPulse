from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="MarketPulse API",
    description="Financial news sentiment API for Indian Stocks",
    version="1.0.0"
)

@app.get("/health")
def health_check():##just a normal Python function. Name doesn't matter to FastAPI, only the decorator matters.
    return{ ## FastAPI takes whatever dict you return and automatically converts it to a JSON response. 
        "status": "ok",
        "service":"MarketPulse",
        "timestamp": datetime.utcnow().isoformat()
    }