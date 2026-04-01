from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.models.api_usage import APIUsage


def test_usage_tracking_logged(client: TestClient, headers):

    db = SessionLocal()

    before = db.query(APIUsage).count()

    client.get("/products", headers=headers)

    after = db.query(APIUsage).count()

    db.close()

    assert after > before