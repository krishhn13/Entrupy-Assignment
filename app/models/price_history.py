from sqlalchemy import Column, Float, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.session import Base

class PriceHistory(Base):
        __tablename__ = "price_history"
        id = Column(
                UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4
        )
        product_id = Column(
                UUID(as_uuid=True),
                ForeignKey("products.id")
        )
        price = Column(
                Float, nullable=False
        )
        source = Column(
                String, nullable=False
        )
        recorded_at = Column(
                DateTime, default=datetime.utcnow
        )