from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.product_service import get_products, get_product_by_id, get_price_history


router = APIRouter(
        prefix="/products",
        tags= ["Products"]
)

@router.get("/")
def list_products(
        source : str | None = Query(default=None),
        category : str | None = Query(default=None),
        min_price : float | None = Query(default=None),
        max_price : float | None = Query(default=None),
        page: int = Query(default=1),
        limit: int = Query(default=20),
        db: Session = Depends(get_db),
):
        products = get_products(
                db,
                source=source,
                category=category,
                min_price=min_price,
                max_price=max_price,
                page = page,
                limit=limit,
        )

        return {
                "page":page,
                "limit":limit,
                "count" : len(products),
                "data" : products
        }

@router.get("/{product_id}")
def product_detail(
        product_id : str,
        db : Session = Depends(get_db)
):
        product = get_product_by_id(db, product_id)
        if not product:
                return {
                        "error" : "Product Not Found"
                }
        return product

@router.get("/{product_id}/history")
def product_price_history(product_id: str, db : Session = Depends(get_db)):
        history = get_price_history(db, product_id)
        if not history:
                return {
                        "message":"No price history found for this product"
                }
        
        return {
                "product_id": product_id,
                "entries": len(history),
                "history": [
                        {
                                "price": h.price,
                                "recorded_at": h.recorded_at,
                                "source": h.source,
                        }
                        for h in history
                ],
        }