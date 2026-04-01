from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product


def total_products(db: Session):
    return db.query(func.count(Product.id)).scalar()


def products_by_source(db: Session):
    results = (
        db.query(Product.source, func.count(Product.id))
        .group_by(Product.source)
        .all()
    )

    return {source: count for source, count in results}


def avg_price_by_category(db: Session):
    results = (
        db.query(Product.category, func.avg(Product.latest_price))
        .group_by(Product.category)
        .all()
    )

    return {
        category: float(avg_price)
        for category, avg_price in results
        if category is not None
    }