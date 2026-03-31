from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.product_service import get_products, get_product_by_id

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
        db: Session = Depends(get_db)
):
        products = get_products(
                db,
                source=source,
                category=category,
                min_price=min_price,
                max_price=max_price
        )

        return {
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