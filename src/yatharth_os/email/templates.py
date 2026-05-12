"""
Email templates for contact request acknowledgement and owner notification.

The templates are intentionally plain text first. This keeps the system simple,
robust, and readable across email clients. HTML templates can be added later.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContactEmailContext:
    """Serializable contact request data required for email rendering."""

    request_id: str
    name: str
    email: str
    company: str | None
    purpose: str
    message: str
    calendly_requested: bool
    calendly_url: str | None = None


def render_acknowledgement_email(context: ContactEmailContext) -> tuple[str, str]:
    """Render requester acknowledgement email subject and body."""

    subject = f"Yatharth OS received your request: {context.request_id}"

    calendly_section = ""
    if context.calendly_requested and context.calendly_url:
        calendly_section = (
            "\nYou can also book a suitable time here:\n" f"{context.calendly_url}\n"
        )

    body = f"""Hi {context.name},

Thanks for reaching out through Yatharth OS.

Your request has been received successfully.

Request ID: {context.request_id}
Purpose: {context.purpose}
Company: {context.company or "N/A"}

Message received:
{context.message}
{calendly_section}
I will review your message and get back if there is a strong fit.

Warm regards,
Yatharth Mahesh Sant
"""

    return subject, body


def render_owner_notification_email(context: ContactEmailContext) -> tuple[str, str]:
    """Render owner notification email subject and body."""

    subject = f"New Yatharth OS contact request: {context.request_id}"

    body = f"""New contact request received.

Request ID: {context.request_id}
Name: {context.name}
Email: {context.email}
Company: {context.company or "N/A"}
Purpose: {context.purpose}
Calendly requested: {context.calendly_requested}

Message:
{context.message}
"""

    return subject, body
