"""
Tests for JWT authentication endpoints.
"""

from uuid import uuid4

from fastapi.testclient import TestClient

from yatharth_os.api.app import app


def _unique_email() -> str:
    return f"user-{uuid4().hex}@example.com"


def test_register_login_and_me_flow() -> None:
    """User should be able to register, login, and access /auth/me."""

    email = _unique_email()
    password = "StrongPass123!"

    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "full_name": "Test User",
                "password": password,
            },
        )

        assert register_response.status_code == 201
        token = register_response.json()["access_token"]
        assert token

        me_response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert me_response.status_code == 200
        assert me_response.json()["email"] == email

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200
        assert login_response.json()["access_token"]


def test_register_duplicate_email_fails() -> None:
    """Registering the same email twice should fail with HTTP 409."""

    email = _unique_email()

    with TestClient(app) as client:
        first_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "full_name": "Duplicate User",
                "password": "StrongPass123!",
            },
        )

        second_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "full_name": "Duplicate User",
                "password": "StrongPass123!",
            },
        )

        assert first_response.status_code == 201
        assert second_response.status_code == 409


def test_login_with_wrong_password_fails() -> None:
    """Login should fail for invalid credentials."""

    email = _unique_email()

    with TestClient(app) as client:
        client.post(
            "/auth/register",
            json={
                "email": email,
                "full_name": "Wrong Password User",
                "password": "StrongPass123!",
            },
        )

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "WrongPass123!",
            },
        )

        assert response.status_code == 401


def test_me_without_token_fails() -> None:
    """Protected user endpoint should reject unauthenticated calls."""

    with TestClient(app) as client:
        response = client.get("/auth/me")

        assert response.status_code == 401
