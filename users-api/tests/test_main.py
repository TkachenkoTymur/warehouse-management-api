from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json()["application_version"] == "1.0.1"

def test_get_users_list():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)