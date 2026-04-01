import json
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.notification_event import NoticationEvent

def ingest_file(file_path: Path, db: Session, source: str):
    with open(file_path, "r", encoding="utf-8") as f:
        item = json.load(f)  # single product snapshot

    external_id = item.get("product_id")
    price = item.get("price")

    existing_product = (
        db.query(Product)
        .filter(Product.external_id == external_id)
        .filter(Product.source == source)
        .first()
    )

    if not existing_product:
        new_product = Product(
            external_id=external_id,
            source=source,
            brand=item.get("brand"),
            model=item.get("model"),
            category=item.get("category"),
            url=item.get("product_url"),
            latest_price=price,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(new_product)
        db.flush()

        price_record = PriceHistory(
            product_id=new_product.id,
            price=price,
            source=source,
        )

        db.add(price_record)

    else:
            if  existing_product.latest_price != price :
                 old_price = existing_product.latest_price
                 existing_product.latest_price = price
                 existing_product.updated_at = datetime.utcnow()

                 price_record = PriceHistory(
                      product_id = existing_product.id,
                      price = price,
                      source = source
                 )
                 db.add(price_record)
                 
                 notification_event = NoticationEvent(
                      product_id = existing_product.id,
                      old_price = old_price,
                      new_price = price,
                 )
                 db.add(notification_event)
    db.commit()