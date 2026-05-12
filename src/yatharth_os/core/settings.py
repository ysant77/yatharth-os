"""
Centralized runtime settings for Yatharth OS.

All environment variables are loaded through this module.

This keeps:
- local development
- Docker
- CI/CD
- staging
- production

consistent and maintainable.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]

# Default local environment
ENV_FILE = os.getenv("YATHARTH_OS_ENV_FILE", ".env")
load_dotenv(BASE_DIR / ENV_FILE)


@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables."""

    environment: str = os.getenv("YATHARTH_OS_ENV", "development")
    debug: bool = os.getenv("YATHARTH_OS_DEBUG", "true").lower() == "true"

    # Database
    database_url: str = os.getenv(
        "YATHARTH_OS_DATABASE_URL",
        "sqlite+aiosqlite:///./yatharth_os.db",
    )

    # Rate limits
    rate_limit_default: str = os.getenv(
        "YATHARTH_OS_RATE_LIMIT_DEFAULT",
        "120/minute",
    )

    rate_limit_auth: str = os.getenv(
        "YATHARTH_OS_RATE_LIMIT_AUTH",
        "20/minute",
    )

    rate_limit_contact: str = os.getenv(
        "YATHARTH_OS_RATE_LIMIT_CONTACT",
        "5/minute",
    )

    # JWT
    jwt_secret_key: str = os.getenv(
        "YATHARTH_OS_JWT_SECRET_KEY",
        "dev-only-secret-change-me",
    )

    jwt_algorithm: str = os.getenv(
        "YATHARTH_OS_JWT_ALGORITHM",
        "HS256",
    )

    jwt_expire_minutes: int = int(
        os.getenv(
            "YATHARTH_OS_JWT_EXPIRE_MINUTES",
            "30",
        )
    )

    # SMTP
    smtp_host: str | None = os.getenv("YATHARTH_OS_SMTP_HOST")

    smtp_port: int = int(
        os.getenv(
            "YATHARTH_OS_SMTP_PORT",
            "587",
        )
    )

    smtp_username: str | None = os.getenv("YATHARTH_OS_SMTP_USERNAME")

    smtp_password: str | None = os.getenv("YATHARTH_OS_SMTP_PASSWORD")

    smtp_from_email: str = os.getenv(
        "YATHARTH_OS_SMTP_FROM_EMAIL",
        "noreply@yatharth-os.local",
    )

    smtp_from_name: str = os.getenv(
        "YATHARTH_OS_SMTP_FROM_NAME",
        "Yatharth OS",
    )

    owner_email: str | None = os.getenv("YATHARTH_OS_OWNER_EMAIL")

    calendly_url: str | None = os.getenv("YATHARTH_OS_CALENDLY_URL")


settings = Settings()
