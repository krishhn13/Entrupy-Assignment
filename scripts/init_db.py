from app.db.session import engine, Base

# Import models so SQLAlchemy registers them
from app.models.product import Product
from app.models.price_history import PriceHistory


def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init()