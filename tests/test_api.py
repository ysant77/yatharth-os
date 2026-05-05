from fastapi.testclient import TestClient

from yatharth_os.api.app import create_app

client = TestClient(create_app())


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_endpoint() -> None:
    response = client.get("/profile")
    assert response.status_code == 200
    assert response.json()["name"] == "Yatharth Mahesh Sant"
