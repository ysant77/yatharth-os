"""
Tests for request ID and correlation ID middleware behavior.
"""

from fastapi.testclient import TestClient

from yatharth_os.api.app import app
from yatharth_os.middleware.request_logging import (
    CORRELATION_ID_HEADER,
    REQUEST_ID_HEADER,
)


def test_request_id_header_is_added() -> None:
    """Every API response should contain an X-Request-ID header."""

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert REQUEST_ID_HEADER in response.headers
    assert response.headers[REQUEST_ID_HEADER]
    assert CORRELATION_ID_HEADER in response.headers
    assert response.headers[CORRELATION_ID_HEADER]


def test_existing_request_id_and_correlation_id_headers_are_preserved() -> None:
    """Caller-provided request and correlation IDs should be preserved."""

    request_id = "test-request-id-123"
    correlation_id = "test-correlation-id-456"

    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={
                REQUEST_ID_HEADER: request_id,
                CORRELATION_ID_HEADER: correlation_id,
            },
        )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id
    assert response.headers[CORRELATION_ID_HEADER] == correlation_id
