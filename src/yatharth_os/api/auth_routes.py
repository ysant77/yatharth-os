"""
Authentication API routes.

The auth API provides a minimal JWT-based flow:
- register user
- login user
- inspect current authenticated user
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from yatharth_os.auth.dependencies import get_current_user
from yatharth_os.auth.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from yatharth_os.auth.service import authenticate_user, create_user, get_user_by_email
from yatharth_os.db.models import User
from yatharth_os.db.session import get_db_session
from yatharth_os.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: UserRegisterRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenResponse:
    """Register a user and return a JWT access token."""

    existing_user = await get_user_by_email(session, payload.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )

    user = await create_user(session, payload)
    token = create_access_token(subject=user.id)

    return TokenResponse(
        access_token=token,
        expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    payload: UserLoginRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""

    user = await authenticate_user(session, payload.email, payload.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=user.id)

    return TokenResponse(
        access_token=token,
        expires_in_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Return the current authenticated user."""

    return UserResponse.model_validate(current_user)
