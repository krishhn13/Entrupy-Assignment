from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.analytics_service import (
    total_products,
    products_by_source,
    avg_price_by_category,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    return {
        "total_products": total_products(db),
        "products_by_source": products_by_source(db),
        "avg_price_by_category": avg_price_by_category(db),
    }