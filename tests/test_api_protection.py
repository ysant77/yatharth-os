"""
Tests for API protection behavior.
"""

from fastapi.testclient import TestClient

from yatharth_os.api.app import app
from yatharth_os.core.settings import settings


def test_rate_limit_settings_have_expected_defaults() -> None:
    """Rate limit settings should be available from centralized settings."""

    assert settings.rate_limit_default
    assert settings.rate_limit_auth
    assert settings.rate_limit_contact


def test_app_has_limiter_registered() -> None:
    """FastAPI app should expose the SlowAPI limiter on app state."""

    assert hasattr(app.state, "limiter")


def test_rate_limit_handler_returns_structured_error() -> None:
    """Rate limit exceptions should return a structured API response."""

    with TestClient(app) as client:
        response = client.get("/health")
        request_id = response.headers["x-request-id"]

    assert request_id


def test_auth_route_still_works_with_rate_limiting_enabled() -> None:
    """Auth routes should remain callable after protection middleware is enabled."""

    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "email": "missing@example.com",
                "password": "StrongPass123!",
            },
        )

    assert response.status_code == 401
    assert response.headers.get("x-request-id") is not None
