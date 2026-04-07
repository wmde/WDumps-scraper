__all__ = ["Scraper"]

from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration


class Scraper:
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session

    def get(
        self, url: str, cache_duration: CacheDuration = CacheDuration.NO_CACHE
    ) -> str:
        response = self.__session.get(url, expire_after=cache_duration.value)
        response.raise_for_status()
        return response.text
