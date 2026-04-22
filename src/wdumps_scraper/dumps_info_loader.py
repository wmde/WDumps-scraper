__all__ = ["DumpsInfoLoader"]

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import wdumps_scraper.rendering as rendering
from wdumps_scraper.cached_limiter_session import CacheDuration
from wdumps_scraper.wdumper_client import ClientError, WDumperClient


class DumpsInfoLoader:
    def __init__(self, client: WDumperClient, max_workers: int = 10) -> None:
        self.__client = client
        self.__max_workers = max_workers

    def load(self, last_id: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        dumps = []
        skipped = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}

            for i in range(last_id, 0, -1):
                future = executor.submit(self.__scrape_dump, i, last_id)
                futures[future] = i

            for future in as_completed(futures):
                id_ = futures[future]
                try:
                    success, result = future.result()
                    if success:
                        dumps.append(result)
                    else:
                        skipped.append(result)
                except Exception as e:
                    skipped.append({"id": id_, "error": str(e)})

        return dumps, skipped

    def __scrape_dump(self, dump_id: int, last_id: int) -> tuple[bool, dict[str, Any]]:
        cache_duration = (
            CacheDuration.INDEFINITE if dump_id < last_id - 10 else CacheDuration.LOW
        )

        try:
            data = self.__client.get_dump(dump_id, cache_duration)
            includes = rendering.render_includes(data["spec"])
            languages = rendering.render_languages(data["spec"])
            statements = rendering.render_statement_filters(data["spec"])
            entities = rendering.render_entity_filters(data["spec"])
            return True, {
                "url": data["url"],
                "id": data["id"],
                "name": data["title"],
                "includes": includes,
                "languages": languages,
                "statement_filters": statements,
                "entity_filters": entities,
            }
        except ClientError as e:
            return False, {"id": dump_id, "error": str(e)}
