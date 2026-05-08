"""
Tests for profile export API endpoints.
"""

from fastapi.testclient import TestClient

from yatharth_os.api.app import app

client = TestClient(app)


def test_export_profile_pdf_endpoint_returns_pdf() -> None:
    """The export endpoint should return PDF content."""

    response = client.get("/export/profile.pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
