from app.db.session import engine, Base

# Import models so SQLAlchemy registers them
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.notification_event import NoticationEvent
from app.models.api_key import APIKey
from app.models.api_usage import APIUsage

def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init()