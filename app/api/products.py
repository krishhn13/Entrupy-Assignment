from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.product_service import (
    get_products,
    get_products_count,
    get_product_by_id,
    get_price_history,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def list_products(
    source: str | None = Query(default=None),
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """
    List products with filtering + pagination support.
    """

    products = get_products(
        db,
        source=source,
        category=category,
        min_price=min_price,
        max_price=max_price,
        page=page,
        limit=limit,
    )

    total = get_products_count(
        db,
        source=source,
        category=category,
        min_price=min_price,
        max_price=max_price,
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": products,
    }


@router.get("/{product_id}")
def product_detail(
    product_id: str,
    db: Session = Depends(get_db),
):
    """
    Get single product details.
    """

    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.get("/{product_id}/history")
def product_price_history(
    product_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve chronological price history for a product.
    """

    history = get_price_history(db, product_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="No price history found for this product"
        )

    # Ensure chronological order for charts
    history = sorted(history, key=lambda h: h.recorded_at)

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