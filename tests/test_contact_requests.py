"""
Tests for protected contact request workflow.
"""

from uuid import uuid4

from fastapi.testclient import TestClient

from yatharth_os.api.app import app


def _register_and_get_token(client: TestClient) -> str:
    email = f"contact-{uuid4().hex}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Contact User",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 201

    return str(response.json()["access_token"])


def test_submit_contact_request_requires_authentication() -> None:
    """Contact request submission should be protected."""

    with TestClient(app) as client:
        response = client.post(
            "/contact-requests",
            json={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "purpose": "collaboration",
                "message": "I would like to discuss an applied AI collaboration.",
            },
        )

    assert response.status_code == 401


def test_submit_contact_request_success() -> None:
    """Authenticated users should be able to submit contact requests."""

    with TestClient(app) as client:
        token = _register_and_get_token(client)

        response = client.post(
            "/contact-requests",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "company": "Example AI Labs",
                "purpose": "collaboration",
                "message": "I would like to discuss an applied AI collaboration.",
                "calendly_requested": True,
            },
        )

    assert response.status_code == 201
    body = response.json()

    assert body["request_id"].startswith("crq_")
    assert body["status"] == "received"


def test_get_contact_request_status_success() -> None:
    """Authenticated users should be able to retrieve their own request."""

    with TestClient(app) as client:
        token = _register_and_get_token(client)

        create_response = client.post(
            "/contact-requests",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "purpose": "career",
                "message": "I would like to discuss a senior AI engineering role.",
            },
        )

        request_id = create_response.json()["request_id"]

        get_response = client.get(
            f"/contact-requests/{request_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert get_response.status_code == 200
    assert get_response.json()["request_id"] == request_id


def test_invalid_contact_request_returns_structured_validation_error() -> None:
    """Invalid POST payloads should return centralized validation errors."""

    with TestClient(app) as client:
        token = _register_and_get_token(client)

        response = client.post(
            "/contact-requests",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "J",
                "email": "not-an-email",
                "purpose": "invalid-purpose",
                "message": "short",
            },
        )

    assert response.status_code == 422
    body = response.json()

    assert body["error"] == "validation_error"
    assert body["request_id"]


def test_bot_trap_field_rejects_payload() -> None:
    """Honeypot field should reject suspicious submissions."""

    with TestClient(app) as client:
        token = _register_and_get_token(client)

        response = client.post(
            "/contact-requests",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "purpose": "other",
                "message": "I would like to discuss your AI engineering work.",
                "website": "https://spam.example.com",
            },
        )

    assert response.status_code == 400


def test_get_missing_contact_request_returns_404() -> None:
    """Unknown contact request IDs should return 404 for authenticated users."""

    with TestClient(app) as client:
        token = _register_and_get_token(client)

        response = client.get(
            "/contact-requests/crq_missing_123",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 404
