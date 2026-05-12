"""
Contact request service layer.

This module owns contact request persistence logic. Routes should remain thin:
validate request -> call service -> return response.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yatharth_os.db.models import ContactRequest, User
from yatharth_os.schemas.contact import ContactRequestCreate


def generate_contact_request_id() -> str:
    """Generate a human-readable external contact request ID."""

    date_part = datetime.now(UTC).strftime("%Y%m%d")
    random_part = uuid4().hex[:10]

    return f"crq_{date_part}_{random_part}"


async def create_contact_request(
    session: AsyncSession,
    payload: ContactRequestCreate,
    user: User,
) -> ContactRequest:
    """Create and persist a contact request for an authenticated user."""

    contact_request = ContactRequest(
        request_id=generate_contact_request_id(),
        user_id=user.id,
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        company=payload.company.strip() if payload.company else None,
        purpose=payload.purpose,
        message=payload.message.strip(),
        status="received",
    )

    session.add(contact_request)
    await session.commit()
    await session.refresh(contact_request)

    return contact_request


async def get_contact_request_for_user(
    session: AsyncSession,
    request_id: str,
    user: User,
) -> ContactRequest | None:
    """Fetch a contact request owned by the authenticated user."""

    result = await session.execute(
        select(ContactRequest).where(
            ContactRequest.request_id == request_id,
            ContactRequest.user_id == user.id,
        )
    )

    return result.scalar_one_or_none()
