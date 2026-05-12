"""
Async email delivery utilities.

If SMTP settings are not configured, emails are logged instead of sent. This
keeps local development and CI safe while still exercising the workflow.
"""

from __future__ import annotations

from email.message import EmailMessage

import aiosmtplib
import structlog

from yatharth_os.core.settings import settings
from yatharth_os.email.templates import (
    ContactEmailContext,
    render_acknowledgement_email,
    render_owner_notification_email,
)

logger = structlog.get_logger(__name__)


def is_smtp_configured() -> bool:
    """Return whether SMTP settings are sufficient for real delivery."""

    return bool(
        settings.smtp_host
        and settings.smtp_username
        and settings.smtp_password
        and settings.smtp_from_email
    )


async def send_email(to_email: str, subject: str, body: str) -> None:
    """Send a plain-text email or log it when SMTP is not configured."""

    if not is_smtp_configured():
        logger.info(
            "email_delivery_skipped",
            reason="smtp_not_configured",
            to_email=to_email,
            subject=subject,
        )
        return

    message = EmailMessage()
    message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        start_tls=True,
    )

    logger.info("email_sent", to_email=to_email, subject=subject)


async def send_contact_request_emails(context: ContactEmailContext) -> None:
    """Send requester acknowledgement and owner notification emails."""

    acknowledgement_subject, acknowledgement_body = render_acknowledgement_email(
        context
    )

    await send_email(
        to_email=context.email,
        subject=acknowledgement_subject,
        body=acknowledgement_body,
    )

    if settings.owner_email:
        owner_subject, owner_body = render_owner_notification_email(context)

        await send_email(
            to_email=settings.owner_email,
            subject=owner_subject,
            body=owner_body,
        )
    else:
        logger.info(
            "owner_notification_skipped",
            reason="owner_email_not_configured",
            request_id=context.request_id,
        )
