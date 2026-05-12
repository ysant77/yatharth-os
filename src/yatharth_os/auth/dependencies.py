"""
FastAPI authentication dependencies.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from yatharth_os.auth.jwt import decode_access_token
from yatharth_os.auth.service import get_user_by_id
from yatharth_os.db.models import User
from yatharth_os.db.session import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """Return the authenticated user for a bearer token."""

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = decode_access_token(token)
    except JWTError as exc:
        raise credentials_error from exc

    user = await get_user_by_id(session, user_id)

    if user is None or not user.is_active:
        raise credentials_error

    return user
