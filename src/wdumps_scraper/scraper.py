from requests.exceptions import HTTPError
from request_cache import CachedSession


class CacheDuration(Enum):
    NO_CACHE = 0
    LOW = 7200
    HIGH = None

class Scraper:
    def __init__(self, session: CachedSession) -> None:
        self.session = session
    
    def get(self, url: str, cache_duration: CacheDuration=CacheDuration.NO_CACHE) -> str:
        response = self.session.get(url, expire_after=cache_duration.value)
        response.raise_for_status()
        return response.text

