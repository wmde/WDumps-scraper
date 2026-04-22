from requests_ratelimiter import SQLiteBucket

from wdumps_scraper import (
    CachedLimiterSession,
    DumpsInfoLoader,
    Scraper,
    ScrapeResult,
    WDumperClient,
    parsing,
)

__all__ = ["WDumpsScraper"]


class WDumpsScraper:
    def __init__(
        self, last_id: int | None, requests_per_second: int = 10, max_workers: int = 5
    ) -> None:
        self.__last_id = last_id
        self.__requests_per_second = requests_per_second
        self.__max_workers = max_workers
        self.__session = CachedLimiterSession(
            "scraper_cache",
            backend="sqlite",
            expire_after=None,
            user_agent="wdumps_scraper/0.1 (https://github.com/wmde/WDumps-scraper)",
            per_second=self.__requests_per_second,
            bucket_class=SQLiteBucket,
            bucket_kwargs={
                "path": "ratelimiter.sqlite",
                "isolation_level": "EXCLUSIVE",
                "check_same_thread": False,
            },
        )
        self.__scraper = Scraper(self.__session)
        self.__dumper_client = WDumperClient(self.__session)
        self.__dumps_info_loader = DumpsInfoLoader(
            self.__dumper_client, max_workers=self.__max_workers
        )

    def run(self) -> ScrapeResult:
        url = "https://wdumps.toolforge.org/dumps"
        html = self.__scraper.get(url)
        last_id = self.__last_id if self.__last_id else parsing.extract_last_id(html)
        return self.__dumps_info_loader.load(last_id)
