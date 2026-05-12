"""
Pydantic schemas for contact requests.

These schemas form the validation contract for the protected contact workflow.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

ContactPurpose = Literal[
    "career",
    "collaboration",
    "consulting",
    "research",
    "recruiting",
    "other",
]


class ContactRequestCreate(BaseModel):
    """Request body for creating a contact request."""

    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    company: str | None = Field(default=None, max_length=255)
    purpose: ContactPurpose
    message: str = Field(min_length=20, max_length=2000)
    calendly_requested: bool = False
    website: str | None = Field(
        default=None,
        max_length=255,
        description="Bot trap field. Real users should leave this empty.",
    )


class ContactRequestResponse(BaseModel):
    """Public response for a submitted contact request."""

    model_config = ConfigDict(from_attributes=True)

    request_id: str
    name: str
    email: EmailStr
    company: str | None
    purpose: str
    message: str
    status: str
    created_at: datetime


class ContactRequestAcceptedResponse(BaseModel):
    """Acknowledgement returned after successful contact request submission."""

    request_id: str
    status: str
    message: str
