from typing import Any, Callable

import pytest
from pytest_mock import MockerFixture

from wdumps_scraper import WDumperClient
from wdumps_scraper.dumps_info_loader import ClientError, DumpsInfoLoader

ClientFactory = Callable[..., WDumperClient]


@pytest.fixture
def make_client(mocker: MockerFixture) -> ClientFactory:
    def factory(responses: list) -> WDumperClient:
        mock_client = mocker.MagicMock(spec=WDumperClient)
        mock_client.get_dump.side_effect = responses
        return mock_client

    return factory


def make_dump(dump_id: int) -> dict[str, Any]:
    return {
        "url": "https://example.com",
        "id": dump_id,
        "title": "All authorship statements",
        "spec": {
            "languages": ["de", "en"],
            "labels": True,
            "descriptions": False,
            "aliases": True,
            "sitelinks": True,
        },
    }


def test_load_all(make_client: ClientFactory) -> None:
    ids = range(1, 11)
    client = make_client([make_dump(i) for i in ids])
    loader = DumpsInfoLoader(client)
    result = loader.load(len(ids))
    assert len(result.dumps) == len(ids)
    assert set(map(lambda d: d["id"], result.dumps)) == set(ids)


def test_partial_fail(make_client: ClientFactory) -> None:
    error = ClientError("kaplow")
    dump = make_dump(2)
    client = make_client([error, dump])
    loader = DumpsInfoLoader(client)
    result = loader.load(2)
    assert len(result.dumps) == 1
    assert len(result.skipped) == 1


def test_all_fail(make_client: ClientFactory) -> None:
    error = ClientError("")
    client = make_client([error, error])
    loader = DumpsInfoLoader(client)
    result = loader.load(2)
    assert len(result.dumps) == 0
    assert len(result.skipped) == 2
