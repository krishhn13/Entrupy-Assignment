from fastapi.testclient import TestClient


def test_price_history(client: TestClient, headers):

    list_response = client.get("/products", headers=headers)
    product_id = list_response.json()["data"][0]["id"]

    response = client.get(
        f"/products/{product_id}/history",
        headers=headers
    )

    assert response.status_code == 200
    assert "history" in response.json()