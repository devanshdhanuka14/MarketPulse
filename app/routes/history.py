from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.tables import SearchHistory

router = APIRouter()

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(SearchHistory)\
        .order_by(SearchHistory.queried_at.desc())\
        .limit(20)\
        .all()
    return [
        {
            "ticker": r.ticker,
            "queried_at": r.queried_at.isoformat(),
            "result_label": r.result_label
        }
        for r in records
    ]