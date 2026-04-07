__all__ = ["WDumperClient"]

import requests

from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration


class WDumperClient:
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session

    def get_dump(
         dump_id: int, cache_duration: CacheDuration=CacheDuration.NO_CACHE
    ) -> str:
        url = f"https://wdumps.toolforge.org/dump/{dump_id}"
        response = requests.get(url, expire_after=cache_duration.value, headers={"Accept":"application/json"})
        response.raise_for_status()
        return response.text