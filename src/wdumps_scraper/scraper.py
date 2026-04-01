import requests

class Scraper:
    def __init__(self, session):
        self.session = session

    class CacheDuration(Enum):
        NO_CACHE = 0
        LOW = 7200
        HIGH = None
    
    def get(url: str, cache_duration: CacheDuration=CacheDuration.NO_CACHE) -> str:
        response = session.get(url, expire_after=cache_duration.value)
        try:
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError:
            raise 

