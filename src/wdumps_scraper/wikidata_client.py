from typing import Mapping

from requests import HTTPError

from wdumps_scraper import ClientError
from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration

__all__ = ["WikidataClient"]


class WikidataClient(Mapping):
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session
        self.__labels: dict[str, str] = {}

    def __getitem__(self, key):
        return self.__labels[key]

    def __iter__(self):
        return iter(self.__labels)

    def __len__(self):
        return len(self.__labels)

    def get_labels(
        self, wd_ids: list, cache_duration: CacheDuration = CacheDuration.NO_CACHE
    ) -> dict[str, str]:
        for wd_id in wd_ids:
            if wd_id not in self.__labels:
                url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={wd_id}&props=labels&languages=en&formatversion=2"
                response = self.__session.get(
                    url,
                    expire_after=cache_duration.value,
                )
                try:
                    response.raise_for_status()
                    data = response.json()
                    label = data["entities"][wd_id]["labels"]["en"]["value"]
                    if label:
                        self.__labels[wd_id] = label
                except HTTPError as e:
                    raise ClientError(e)
        return self.__labels
