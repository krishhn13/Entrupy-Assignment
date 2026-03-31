from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.session import Base

class Product(Base) :
        __tablename__ = "products"

        id = Column(
                UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4
        )
        external_id = Column(
                String, index=True
        )
        brand = Column(String, index=True)
        model = Column(String)
        category = Column(String, index=True)
        url = Column(String)
        latest_price = Column(Float)
        created_at = Column(DateTime, default=datetime.utcnow)
        update_at = Column(DateTime, default=datetime.utcnow)


