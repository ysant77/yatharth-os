"""
Protected contact request API routes.

Authenticated users can submit contact/collaboration requests and retrieve their
own request status.
"""

from typing import Annotated

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from yatharth_os.auth.dependencies import get_current_user
from yatharth_os.contact.service import (
    create_contact_request,
    get_contact_request_for_user,
)
from yatharth_os.core.limiter import limiter
from yatharth_os.core.settings import settings
from yatharth_os.db.models import User
from yatharth_os.db.session import get_db_session
from yatharth_os.email.mailer import send_contact_request_emails
from yatharth_os.email.templates import ContactEmailContext
from yatharth_os.schemas.contact import (
    ContactRequestAcceptedResponse,
    ContactRequestCreate,
    ContactRequestResponse,
)

router = APIRouter(prefix="/contact-requests", tags=["contact-requests"])
logger = structlog.get_logger(__name__)


@router.post(
    "",
    response_model=ContactRequestAcceptedResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(settings.rate_limit_contact)
async def submit_contact_request(
    request: Request,
    background_tasks: BackgroundTasks,
    payload: ContactRequestCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ContactRequestAcceptedResponse:
    """Create a protected contact request for the authenticated user."""

    if payload.website:
        logger.warning(
            "contact_request_bot_trap_triggered",
            user_id=current_user.id,
            email=current_user.email,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid contact request payload.",
        )

    contact_request = await create_contact_request(
        session=session,
        payload=payload,
        user=current_user,
    )

    email_context = ContactEmailContext(
        request_id=contact_request.request_id,
        name=contact_request.name,
        email=contact_request.email,
        company=contact_request.company,
        purpose=contact_request.purpose,
        message=contact_request.message,
        calendly_requested=payload.calendly_requested,
        calendly_url=settings.calendly_url,
    )

    background_tasks.add_task(send_contact_request_emails, email_context)

    logger.info(
        "contact_request_created",
        request_id=getattr(request.state, "request_id", None),
        correlation_id=getattr(request.state, "correlation_id", None),
        contact_request_id=contact_request.request_id,
        user_id=current_user.id,
        purpose=contact_request.purpose,
        email_acknowledgement_queued=True,
    )

    return ContactRequestAcceptedResponse(
        request_id=contact_request.request_id,
        status=contact_request.status,
        message=(
            "Thanks. Your request has been received. "
            "An acknowledgement email will be sent if email delivery is configured."
        ),
    )


@router.get("/{request_id}", response_model=ContactRequestResponse)
async def get_contact_request_status(
    request_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ContactRequestResponse:
    """Return a contact request owned by the authenticated user."""

    contact_request = await get_contact_request_for_user(
        session=session,
        request_id=request_id,
        user=current_user,
    )

    if contact_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact request not found.",
        )

    return ContactRequestResponse.model_validate(contact_request)
