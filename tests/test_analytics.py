from fastapi.testclient import TestClient


def test_analytics_summary(client: TestClient, headers):

    response = client.get(
        "/analytics/summary",
        headers=headers
    )

    assert response.status_code == 200
    assert "total_products" in response.json()