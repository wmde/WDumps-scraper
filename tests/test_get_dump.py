import json
from typing import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from requests import HTTPError

from wdumps_scraper.wdumper_client import ClientError, WDumperClient

MOCK_DUMP = {
    "dump": {
        "id": 19,
        "title": "All authorship statements",
        "spec": json.dumps(
            {"labels": True, "descriptions": False, "aliases": True, "sitelinks": True}
        ),
    }
}


@pytest.fixture
def make_mock_session(mocker: MockerFixture) -> Callable[..., MagicMock]:
    def factory(status_code: int = 200, payload: dict = MOCK_DUMP) -> MagicMock:
        mock_response = mocker.MagicMock()
        mock_response.status_code = status_code

        if status_code != 200:
            mock_response.raise_for_status.side_effect = HTTPError(
                f"HTTP {status_code}"
            )

        mock_response.json.return_value = payload
        mock_session = mocker.MagicMock()
        mock_session.get.return_value = mock_response
        return mock_session

    return factory


def test_get_dump_returns_dict(make_mock_session: Callable[..., MagicMock]) -> None:
    session = make_mock_session(status_code=200, payload=MOCK_DUMP)
    dumper_client = WDumperClient(session)
    result = dumper_client.get_dump(1)
    assert result["id"] == MOCK_DUMP["dump"]["id"]
    assert result["title"] == MOCK_DUMP["dump"]["title"]
    assert "labels" in result["spec"]
    assert "descriptions" in result["spec"]
    assert "aliases" in result["spec"]
    assert "sitelinks" in result["spec"]
    assert result["url"] == "https://wdumps.toolforge.org/dump/1"


def test_get_dumps_raises_on_bad_json(
    make_mock_session: Callable[..., MagicMock],
) -> None:
    session = make_mock_session(
        status_code=200, payload={"dump": {"spec": "regular string"}}
    )
    dumper_client = WDumperClient(session)

    with pytest.raises(ClientError):
        dumper_client.get_dump(1)


def test_get_dumps_raises_on_bad_status(
    make_mock_session: Callable[..., MagicMock],
) -> None:
    session = make_mock_session(status_code=400)
    dumper_client = WDumperClient(session)

    with pytest.raises(ClientError):
        dumper_client.get_dump(1)
