"""
Rate limiting configuration.

SlowAPI is used because it integrates cleanly with FastAPI/Starlette and keeps
this first protection phase lightweight. Later, this can be replaced with
Redis-backed distributed rate limiting for multi-worker deployments.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from yatharth_os.core.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit_default],
)
