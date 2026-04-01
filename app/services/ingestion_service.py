import json
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.notification_event import NotificationEvent


def ingest_file(file_path: Path, db: Session, source: str):

    # Load snapshot JSON
    with open(file_path, "r", encoding="utf-8") as f:
        item = json.load(f)

    external_id = item.get("product_id")
    price = item.get("price")

    if external_id is None or price is None:
        return

    # Extract snapshot index from filename
    # Example: 1stdibs_chanel_belts_07.json → 7
    try:
        snapshot_index = int(file_path.stem.split("_")[-1])
    except Exception:
        snapshot_index = 1

    # Convert snapshot index into timeline timestamp
    recorded_at = datetime.utcnow() - timedelta(days=(30 - snapshot_index))

    existing_product = (
        db.query(Product)
        .filter(Product.external_id == external_id)
        .first()
    )

    # CASE 1: New product
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
            recorded_at=recorded_at,
        )

        db.add(price_record)

    # CASE 2: Existing product snapshot update
    else:

        old_price = existing_product.latest_price

        # Always store snapshot as history entry
        price_record = PriceHistory(
            product_id=existing_product.id,
            price=price,
            source=source,
            recorded_at=recorded_at,
        )

        db.add(price_record)

        # Only trigger notification if price changed
        if old_price != price:

            existing_product.latest_price = price
            existing_product.updated_at = datetime.utcnow()

            notification_event = NotificationEvent(
                product_id=existing_product.id,
                old_price=old_price,
                new_price=price,
            )

            db.add(notification_event)

    db.commit()