from sqlalchemy.orm import Session
from app.models.product import Product

def get_products(
                db : Session,
                source : str | None= None,
                category : str | None=None,
                min_price : float | None=None,
                max_price : float | None=None,
):
        query = db.query(Product)
        if source :
                query = query.filter(Product.source == source)

        if category:
                query = query.filter(Product.category == category)
        
        if min_price is not None: 
                query = query.filter(Product.latest_price >= min_price)
        
        if max_price is not None:
                query = query.filter(Product.latest_price<=max_price)

        return query.all()

def get_product_by_id(db: Session, product_id: str):
        return db.query(Product).filter(
                Product.id == product_id
        ).first()