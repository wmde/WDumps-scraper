from requests import HTTPError

from wdumps_scraper import ClientError
from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration

__all__ = ["WikidataClient"]


class WikidataClient:
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session

    def get_label(
        self, wd_id: str, cache_duration: CacheDuration = CacheDuration.NO_CACHE
    ) -> str:
        url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={wd_id}&props=labels&languages=en&formatversion=2"
        response = self.__session.get(
            url,
            expire_after=cache_duration.value,
        )
        try:
            response.raise_for_status()
            data = response.json()
            label = data["entities"][wd_id]["labels"]["en"]["value"]
            return f"'{label}'" if label else wd_id
        except HTTPError as e:
            raise ClientError(e)
