from fastapi.testclient import TestClient

def test_refresh_endpoint(client, headers):
    response = client.post("/refresh", headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "refresh completed"