import json
from typing import Any

from requests import HTTPError

from wdumps_scraper.cached_limiter_session import CachedLimiterSession, CacheDuration
from wdumps_scraper.exceptions import ClientError

__all__ = ["WikidataClient"]


class WikidataClient:
    def __init__(self, session: CachedLimiterSession) -> None:
        self.__session = session
        self.__base_url = "https://www.wikidata.org/w/api.php"

    def __action(
        self,
        action: str,
        params: dict[str, Any],
        cache_duration: CacheDuration = CacheDuration.TWO_WEEKS,
    ) -> Any:
        return self.__session.get(
            url=self.__base_url,
            params={"action": action, "format": "json", "formatversion": 2, **params},
            headers={"Accept": "application/json"},
            expire_after=cache_duration,
        )

    def get_labels(self, wd_ids: list) -> dict[str, str]:
        response = self.__action(
            "wbgetentities",
            {
                "ids": "|".join(sorted(wd_ids)),
                "props": "labels",
                "languages": "en",
                "languagefallback": True,
            },
        )
        try:
            response.raise_for_status()
            data = response.json()
            return {
                e_id: e.get("labels", {}).get("en", {}).get("value")
                for e_id, e in data.get("entities", {}).items()
                if len(e.get("labels")) > 0
            }
        except (json.JSONDecodeError, HTTPError) as e:
            raise ClientError(e)
