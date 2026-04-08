__all__ = ["WDumperClient"]

import json

from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration


class WDumperClient:
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session

    def get_dump(
        self, dump_id: int, cache_duration: CacheDuration = CacheDuration.NO_CACHE
    ) -> str:
        url = f"https://wdumps.toolforge.org/dump/{dump_id}"
        response = self.__session.get(
            url,
            expire_after=cache_duration.value,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        spec = json.loads(response.json()["dump"]["spec"])
        return spec
