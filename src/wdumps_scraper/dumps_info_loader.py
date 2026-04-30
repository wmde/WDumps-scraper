import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, NamedTuple, TypedDict

import wdumps_scraper.rendering as rendering
from wdumps_scraper.cached_limiter_session import CacheDuration
from wdumps_scraper.wdumper_client import ClientError, WDumperClient
from wdumps_scraper.wikidata_client import WikidataClient

__all__ = ["DumpsInfoLoader"]


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
    def __init__(
        self,
        client: WDumperClient,
        wikidata_client: WikidataClient | None = None,
        max_workers: int = 10,
    ) -> None:
        self.__client = client
        self.__wikidata_client = wikidata_client
        self.__max_workers = max_workers

    def load(self, last_id: int) -> ScrapeResult:
        dumps = []
        struct_dumps = []
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

        wd_ids = sorted(self.__extract_ids(dumps))

        if self.__wikidata_client:
            labels: dict = {}
            for i in range(0, len(wd_ids), 50):
                labels.update(self.__wikidata_client.get_labels(wd_ids[i:50]))

        for i in range(0, len(dumps)):
            struct_dumps.append(self.__render(dumps[i]))

        return ScrapeResult(struct_dumps, skipped)

    def __scrape_dump(self, dump_id: int, last_id: int) -> dict[str, Any]:
        cache_duration = (
            CacheDuration.INDEFINITE
            if dump_id < last_id - 10
            else CacheDuration.TWO_HOURS
        )
        return self.__client.get_dump(dump_id, cache_duration)

    def __extract_ids(self, dumps: list) -> set:
        wd_ids: set = set()
        pattern = "^[Q|P]\\d+$"

        for i in range(0, len(dumps)):
            entities = dumps[i].get("spec").get("entities") or []
            for j in range(0, len(entities)):
                properties = entities[j].get("properties")
                for k in range(0, len(properties)):
                    property_filters = [
                        properties[k].get(x) for x in ["property", "value"]
                    ]
                    wd_ids.update(
                        p
                        for p in property_filters
                        if property_filters and re.match(pattern, str(p), re.IGNORECASE)
                    )
            statements = dumps[i].get("spec").get("statements") or []
            for j in range(0, len(statements)):
                statement_filters = statements[j].get("properties") or []
                wd_ids.update(
                    s
                    for s in statement_filters
                    if statement_filters and re.match(pattern, str(s), re.IGNORECASE)
                )

        return wd_ids

    def __render(self, data: dict[str, Any]) -> DumpInfo:
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
