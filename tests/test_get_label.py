from typing import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from requests import HTTPError

from wdumps_scraper import ClientError, WikidataClient

MOCK_ENTITIES = {
    "entities": {"Q34969": {"labels": {"en": {"value": "Benjamin Franklin"}}}}
}
MOCK_ENTITIES_NO_LABEL = {"entities": {"Q34969": {"labels": {"en": {"value": ""}}}}}


@pytest.fixture
def make_mock_session(mocker: MockerFixture) -> Callable[..., MagicMock]:
    def factory(status_code: int = 200, payload: dict = MOCK_ENTITIES) -> MagicMock:
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


def test_get_label_returns_str(make_mock_session: Callable[..., MagicMock]) -> None:
    session = make_mock_session(status_code=200, payload=MOCK_ENTITIES)
    wikidata_client = WikidataClient(session)
    result = wikidata_client.get_label("Q34969")
    assert result == "'Benjamin Franklin'"


def test_get_label_no_label(make_mock_session: Callable[..., MagicMock]) -> None:
    session = make_mock_session(status_code=200, payload=MOCK_ENTITIES_NO_LABEL)
    wikidata_client = WikidataClient(session)
    result = wikidata_client.get_label("Q34969")
    assert result == "Q34969"


def test_get_label_raises_on_bad_status(
    make_mock_session: Callable[..., MagicMock],
) -> None:
    session = make_mock_session(status_code=400)
    wikidata_client = WikidataClient(session)

    with pytest.raises(ClientError):
        wikidata_client.get_label("Q1")
