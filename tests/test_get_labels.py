from typing import Any, Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from requests import HTTPError

from wdumps_scraper import ClientError, WikidataClient

MOCK_ENTITIES_SINGLE = {"entities": {"Q1": {"labels": {"en": {"value": "Saturn"}}}}}
MOCK_ENTITIES_MULTIPLE = {
    "entities": {
        "Q1": {"labels": {"en": {"value": "Saturn"}}},
        "Q4": {"labels": {"en": {"value": "Mars"}}},
    }
}
MOCK_ENTITIES_NO_LABEL: dict[str, dict[str, dict[str, dict]]] = {
    "entities": {"Q2": {"labels": {}}}
}


@pytest.fixture
def make_mock_session(mocker: MockerFixture) -> Callable[..., MagicMock]:
    def factory(
        status_code: int = 200, payload: dict[str, Any] | None = None
    ) -> MagicMock:
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


@pytest.mark.parametrize(
    "response, expected",
    [
        (MOCK_ENTITIES_SINGLE, {"Q1": "Saturn"}),
        (MOCK_ENTITIES_NO_LABEL, {}),
        (MOCK_ENTITIES_MULTIPLE, {"Q1": "Saturn", "Q4": "Mars"}),
    ],
)
def test_get_labels_returns_dict(
    make_mock_session: Callable[..., MagicMock],
    response: dict[str, Any],
    expected: dict[str, str],
) -> None:
    session = make_mock_session(status_code=200, payload=response)
    wikidata_client = WikidataClient(session)
    result = wikidata_client.get_labels([])
    assert result == expected


def test_get_labels_raises_on_bad_status(
    make_mock_session: Callable[..., MagicMock],
) -> None:
    session = make_mock_session(status_code=400)
    wikidata_client = WikidataClient(session)

    with pytest.raises(ClientError):
        wikidata_client.get_labels([])
