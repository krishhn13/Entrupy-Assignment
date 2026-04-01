from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct

from app.db.deps import get_db
from app.models.product import Product

router = APIRouter(prefix="/meta", tags = ["Metadata"])

@router.get("/categories")
def get_categories(db:Session = Depends(get_db)):
        categories = db.query(
                distinct(Product.category)
        ).all()

        return [c[0] for c in categories if c[0]]


@router.get("/sources")
def get_sources(db:Session = Depends(get_db)):
        sources = db.query(distinct(Product.source)).all()
        return [s[0] for s in sources if s[0]]