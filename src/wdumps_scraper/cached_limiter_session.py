from enum import Enum
from typing import Any

from requests import Session
from requests_cache import DO_NOT_CACHE, NEVER_EXPIRE, CacheMixin
from requests_ratelimiter import LimiterMixin

__all__ = ["CachedLimiterSession", "CacheDuration"]


class CacheDuration(Enum):
    NO_CACHE = DO_NOT_CACHE
    TWO_HOURS = 7200
    TWO_WEEKS = 60 * 60 * 24 * 14
    INDEFINITE = NEVER_EXPIRE


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    def __init__(
        self, *args: Any, user_agent: str | None = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        if user_agent is not None:
            self.headers.update({"User-Agent": user_agent})
