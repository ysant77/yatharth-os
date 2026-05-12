"""
Authentication service layer.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from yatharth_os.auth.hashing import hash_password, verify_password
from yatharth_os.db.models import User
from yatharth_os.schemas.auth import UserRegisterRequest


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Fetch a user by email address."""

    result = await session.execute(select(User).where(User.email == email.lower()))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: str) -> User | None:
    """Fetch a user by primary key."""

    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, payload: UserRegisterRequest) -> User:
    """Create and persist a new user."""

    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    """Validate email/password credentials and return the user if valid."""

    user = await get_user_by_email(session, email)

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
