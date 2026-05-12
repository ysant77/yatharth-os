"""
Application settings for Yatharth OS.

This module centralizes environment-driven settings so future phases do not
scatter environment variable reads across routes, services, and middleware.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables."""

    rate_limit_default: str = os.getenv("YATHARTH_OS_RATE_LIMIT_DEFAULT", "120/minute")
    rate_limit_auth: str = os.getenv("YATHARTH_OS_RATE_LIMIT_AUTH", "20/minute")
    rate_limit_contact: str = os.getenv("YATHARTH_OS_RATE_LIMIT_CONTACT", "5/minute")


settings = Settings()
