import json
from typing import Any

from requests.exceptions import HTTPError

from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration

__all__ = ["WDumperClient", "ClientError"]


class ClientError(Exception):
    pass


class WDumperClient:
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session

    def get_dump(
        self, dump_id: int, cache_duration: CacheDuration = CacheDuration.NO_CACHE
    ) -> dict[str, Any]:
        url = f"https://wdumps.toolforge.org/dump/{dump_id}"
        response = self.__session.get(
            url,
            headers={"Accept": "application/json"},
            expire_after=cache_duration.value,
        )
        try:
            response.raise_for_status()
            data = response.json()
            dump = data["dump"]
            dump["spec"] = json.loads(dump["spec"])
            dump["url"] = url
            return dump
        except (json.JSONDecodeError, HTTPError) as e:
            raise ClientError(e)
