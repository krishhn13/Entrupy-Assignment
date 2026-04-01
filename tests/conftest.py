import pytest
import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from app.main import app

load_dotenv()

API_KEY = os.getenv("DEFAULT_API_KEY")

@pytest.fixture
def client():
        return TestClient(app)

@pytest.fixture
def headers():
        return {
                "x-api-key" : API_KEY
        }