"""
Tests for email template rendering.
"""

from yatharth_os.email.templates import (
    ContactEmailContext,
    render_acknowledgement_email,
    render_owner_notification_email,
)


def _context() -> ContactEmailContext:
    return ContactEmailContext(
        request_id="crq_20260512_test",
        name="Jane Doe",
        email="jane@example.com",
        company="Example AI Labs",
        purpose="collaboration",
        message="I would like to discuss an applied AI collaboration.",
        calendly_requested=True,
        calendly_url="https://calendly.com/example",
    )


def test_acknowledgement_email_contains_request_details() -> None:
    """Acknowledgement email should include request ID and message context."""

    subject, body = render_acknowledgement_email(_context())

    assert "crq_20260512_test" in subject
    assert "Jane Doe" in body
    assert "collaboration" in body
    assert "https://calendly.com/example" in body


def test_owner_notification_email_contains_submitter_details() -> None:
    """Owner notification should include submitter details."""

    subject, body = render_owner_notification_email(_context())

    assert "New Yatharth OS contact request" in subject
    assert "jane@example.com" in body
    assert "Example AI Labs" in body
