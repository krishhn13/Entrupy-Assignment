from fastapi.testclient import TestClient


def test_missing_api_key(client: TestClient):

    response = client.get("/products")

    assert response.status_code == 401