from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.session import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(
                UUID(as_uuid=True), 
                primary_key=True, 
                default=uuid.uuid4,
        )

    key = Column(String, unique=True, nullable=False)

    owner = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)