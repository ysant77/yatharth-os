"""
Tests for email delivery behavior.
"""

from dataclasses import replace

import pytest

from yatharth_os.core.settings import settings
from yatharth_os.email.mailer import send_email


def test_smtp_is_not_configured_by_default(monkeypatch) -> None:
    """SMTP should be treated as disabled when required settings are missing."""

    from yatharth_os.email import mailer

    patched_settings = replace(
        settings,
        smtp_host=None,
        smtp_port=None,
        smtp_username=None,
        smtp_password=None,
        smtp_from_email=None,
    )

    monkeypatch.setattr(mailer, "settings", patched_settings)

    assert mailer.is_smtp_configured() is False


@pytest.mark.anyio
async def test_send_email_skips_when_smtp_not_configured() -> None:
    """Sending email without SMTP config should not crash."""

    await send_email(
        to_email="jane@example.com",
        subject="Test email",
        body="Hello",
    )
