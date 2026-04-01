from fastapi.testclient import TestClient


def test_products_list(client: TestClient, headers):
    response = client.get("/products", headers=headers)

    assert response.status_code == 200
    assert "data" in response.json()


def test_products_filtering(client: TestClient, headers):
    response = client.get(
        "/products?source=grailed",
        headers=headers
    )

    assert response.status_code == 200


def test_product_detail(client: TestClient, headers):
    list_response = client.get("/products", headers=headers)
    product_id = list_response.json()["data"][0]["id"]

    detail_response = client.get(
        f"/products/{product_id}",
        headers=headers
    )

    assert detail_response.status_code == 200