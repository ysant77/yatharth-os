"""
Pydantic schemas for authentication endpoints.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Request body for user registration."""

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserLoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class UserResponse(BaseModel):
    """Safe user response without password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    is_active: bool
