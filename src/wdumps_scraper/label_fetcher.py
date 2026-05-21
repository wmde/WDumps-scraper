from typing import Protocol, runtime_checkable

from wdumps_scraper.wikidata_client import WikidataClient

__all__ = ["LabelFetcher", "NullLabelFetcher", "BatchLabelFetcher"]


@runtime_checkable
class LabelFetcher(Protocol):
    def fetch(self, ids: list[str]) -> dict[str, str]: ...


class NullLabelFetcher:
    # noinspection PyMethodMayBeStatic
    def fetch(self, _ids: list[str]) -> dict[str, str]:
        return {}


class BatchLabelFetcher:
    def __init__(self, wikidata_client: WikidataClient) -> None:
        self.__client = wikidata_client

    def fetch(self, ids: list[str]) -> dict[str, str]:
        labels: dict = {}
        sorted_ids = sorted(ids)
        for i in range(0, len(sorted_ids), 50):
            labels.update(self.__client.get_labels(sorted_ids[i : i + 50]))
        return labels
