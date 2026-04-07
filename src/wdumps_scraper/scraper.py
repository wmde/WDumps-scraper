from enum import Enum

import requests_cache


class CacheDuration(Enum):
    NO_CACHE = 0
    LOW = 7200
    HIGH = None

class Scraper:
    def __init__(self, session: requests_cache.CachedSession) -> None:
        self.__session = session
    
    def get(
            self, url: str, cache_duration: CacheDuration=CacheDuration.NO_CACHE
    ) -> str:
        response = self.__session.get(url, expire_after=cache_duration.value)
        response.raise_for_status()
        return response.text

