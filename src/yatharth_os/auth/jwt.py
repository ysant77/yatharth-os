"""
JWT creation and decoding helpers.

For this learning project we use a signed access token with a short expiry.
Refresh tokens and token revocation can be added later when the application
needs browser/mobile-grade session management.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

JWT_SECRET_KEY = os.getenv(
    "YATHARTH_OS_JWT_SECRET_KEY",
    "dev-only-change-this-secret-in-production",
)
JWT_ALGORITHM = os.getenv("YATHARTH_OS_JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("YATHARTH_OS_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token."""

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> str:
    """Decode an access token and return the subject/user id."""

    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

    token_type = payload.get("type")
    subject = payload.get("sub")

    if token_type != "access" or not isinstance(subject, str):
        raise JWTError("Invalid access token payload")

    return subject
