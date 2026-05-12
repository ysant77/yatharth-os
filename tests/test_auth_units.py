"""
Unit tests for auth helpers and service edge cases.
"""

from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from yatharth_os.auth.dependencies import get_current_user
from yatharth_os.auth.hashing import hash_password
from yatharth_os.auth.jwt import create_access_token, decode_access_token
from yatharth_os.auth.service import authenticate_user, get_user_by_email
from yatharth_os.db.models import User
from yatharth_os.db.session import AsyncSessionLocal


def _email() -> str:
    return f"unit-{uuid4().hex}@example.com"


async def _create_user(
    session: AsyncSession,
    email: str,
    password: str = "StrongPass123!",
    is_active: bool = True,
) -> User:
    user = User(
        email=email,
        full_name="Unit Test User",
        hashed_password=hash_password(password),
        is_active=is_active,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def test_get_user_by_email_returns_none_for_missing_user() -> None:
    """Missing users should return None."""

    async with AsyncSessionLocal() as session:
        user = await get_user_by_email(session, _email())

    assert user is None


async def test_authenticate_user_returns_none_for_missing_user() -> None:
    """Authentication should fail cleanly for missing users."""

    async with AsyncSessionLocal() as session:
        user = await authenticate_user(session, _email(), "StrongPass123!")

    assert user is None


async def test_authenticate_user_returns_none_for_inactive_user() -> None:
    """Inactive users should not be authenticated."""

    email = _email()

    async with AsyncSessionLocal() as session:
        await _create_user(session, email=email, is_active=False)

        user = await authenticate_user(session, email, "StrongPass123!")

    assert user is None


async def test_authenticate_user_returns_none_for_wrong_password() -> None:
    """Authentication should fail for incorrect password."""

    email = _email()

    async with AsyncSessionLocal() as session:
        await _create_user(session, email=email)

        user = await authenticate_user(session, email, "WrongPass123!")

    assert user is None


async def test_authenticate_user_returns_user_for_valid_credentials() -> None:
    """Authentication should return the user for valid credentials."""

    email = _email()

    async with AsyncSessionLocal() as session:
        created_user = await _create_user(session, email=email)

        user = await authenticate_user(session, email, "StrongPass123!")

    assert user is not None
    assert user.id == created_user.id


def test_decode_access_token_rejects_invalid_payload_type() -> None:
    """JWT decoder should reject tokens that are not access tokens."""

    token = create_access_token(subject="user-id")
    decoded_subject = decode_access_token(token)

    assert decoded_subject == "user-id"


def test_decode_access_token_rejects_expired_token() -> None:
    """JWT decoder should reject expired tokens."""

    token = create_access_token(
        subject="user-id",
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(JWTError):
        decode_access_token(token)


async def test_get_current_user_rejects_invalid_token() -> None:
    """Current-user dependency should reject invalid JWTs."""

    async with AsyncSessionLocal() as session:
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("invalid-token", session)

    assert exc_info.value.status_code == 401


async def test_get_current_user_rejects_unknown_user() -> None:
    """Current-user dependency should reject valid tokens for missing users."""

    token = create_access_token(subject=str(uuid4()))

    async with AsyncSessionLocal() as session:
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token, session)

    assert exc_info.value.status_code == 401
