from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, NamedTuple, TypedDict

import wdumps_scraper.rendering as rendering
from wdumps_scraper.cached_limiter_session import CacheDuration
from wdumps_scraper.wdumper_client import ClientError, WDumperClient

__all__ = ["DumpsInfoLoader", "ClientError"]


class DumpInfo(TypedDict):
    url: str
    id: int
    name: str
    includes: str
    languages: str
    statement_filters: str
    entity_filters: str


class ScrapeResult(NamedTuple):
    dumps: list[DumpInfo]
    skipped: list[dict[str, Any]]


class DumpsInfoLoader:
    def __init__(self, client: WDumperClient, max_workers: int = 10) -> None:
        self.__client = client
        self.__max_workers = max_workers

    def load(self, last_id: int) -> ScrapeResult:
        dumps = []
        skipped = []

        with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:
            futures = {}

            for i in range(last_id, 0, -1):
                future = executor.submit(self.__scrape_dump, i, last_id)
                futures[future] = i

            for future in as_completed(futures):
                id_: int = futures[future]
                try:
                    result = future.result()
                    dumps.append(result)
                except ClientError as e:
                    skipped.append({"id": id_, "error": str(e)})

        return ScrapeResult(dumps, skipped)

    def __scrape_dump(self, dump_id: int, last_id: int) -> DumpInfo:
        cache_duration = (
            CacheDuration.INDEFINITE if dump_id < last_id - 10 else CacheDuration.LOW
        )

        data = self.__client.get_dump(dump_id, cache_duration)
        includes = rendering.render_includes(data["spec"])
        languages = rendering.render_languages(data["spec"])
        statements = rendering.render_statement_filters(data["spec"])
        entities = rendering.render_entity_filters(data["spec"])
        return {
            "url": data["url"],
            "id": data["id"],
            "name": data["title"],
            "includes": includes,
            "languages": languages,
            "statement_filters": statements,
            "entity_filters": entities,
        }
