from typing import Any

from requests_ratelimiter import SQLiteBucket

from wdumps_scraper import parsing
from wdumps_scraper.cached_limiter_session import CachedLimiterSession
from wdumps_scraper.dumps_info_loader import DumpsInfoLoader, ScrapeResult
from wdumps_scraper.label_fetcher import (
    BatchLabelFetcher,
    LabelFetcher,
    NullLabelFetcher,
)
from wdumps_scraper.scraper import Scraper
from wdumps_scraper.wdumper_client import WDumperClient
from wdumps_scraper.wikidata_client import WikidataClient

__all__ = ["WDumpsScraper"]


class WDumpsScraper:
    def __init__(
        self,
        last_id: int | None,
        requests_per_second: int = 10,
        max_workers: int = 5,
        label_resolution: bool = False,
    ) -> None:
        self.__last_id = last_id
        self.__requests_per_second = requests_per_second
        self.__max_workers = max_workers
        self.__label_resolution = label_resolution
        self.__session = self.__make_scraper_session()
        self.__scraper = Scraper(self.__session)
        self.__dumper_client = WDumperClient(self.__session)
        self.__label_fetcher = self.__make_label_fetcher()
        self.__dumps_info_loader = DumpsInfoLoader(
            self.__dumper_client,
            self.__label_fetcher,
            self.__max_workers,
        )

    def run(self) -> ScrapeResult:
        url = "https://wdumps.toolforge.org/dumps"
        html = self.__scraper.get(url)
        last_id = self.__last_id if self.__last_id else parsing.extract_last_id(html)
        return self.__dumps_info_loader.load(last_id)

    @property
    def __session_kwargs(self) -> dict[str, Any]:
        return {
            "cache_name": "scraper_cache",
            "backend": "sqlite",
            "expire_after": None,
            "user_agent": "wdumps_scraper/0.1 (https://github.com/wmde/WDumps-scraper)",
            "bucket_class": SQLiteBucket,
            "bucket_kwargs": {
                "path": "ratelimiter.sqlite",
                "isolation_level": "EXCLUSIVE",
                "check_same_thread": False,
            },
        }

    def __make_scraper_session(self) -> CachedLimiterSession:
        kwargs = self.__session_kwargs
        return CachedLimiterSession(**kwargs, per_second=self.__requests_per_second)

    def __make_wikidata_session(self) -> CachedLimiterSession:
        kwargs = self.__session_kwargs
        kwargs["bucket_kwargs"]["name"] = "wikidata"
        return CachedLimiterSession(**kwargs, per_second=3)

    def __make_label_fetcher(self) -> LabelFetcher:
        if self.__label_resolution:
            client = WikidataClient(self.__make_wikidata_session())
            return BatchLabelFetcher(client)
        return NullLabelFetcher()
