"""
Tests for FastAPI portfolio endpoints.
"""

from fastapi.testclient import TestClient

from yatharth_os.api.app import app

client = TestClient(app)


def test_health_check() -> None:
    """Health endpoint should return service status."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_endpoint() -> None:
    """Profile endpoint should return structured profile data."""

    response = client.get("/profile")

    assert response.status_code == 200
    assert response.json()["name"] == "Yatharth Mahesh Sant"


def test_projects_endpoint() -> None:
    """Projects endpoint should return project list."""

    response = client.get("/projects")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_projects_filter_endpoint() -> None:
    """Projects endpoint should support tag filtering."""

    response = client.get("/projects?tag=rag")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_experience_endpoint() -> None:
    """Experience endpoint should return experience entries."""

    response = client.get("/experience")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
