from collections.abc import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from wdumps_scraper.scraper import Scraper

MOCK_HTML = """
<p>Test Passed</p>
"""

@pytest.fixture
def make_mock_session(
        mocker: MockerFixture
) -> Callable[MockerFixture, MagicMock]:
    def factory(
        status_code: int = 200,
        text: str = "<p>Hello</p>"
    ) -> MagicMock:
        mock_response = mocker.MagicMock()
        mock_response.text = text
        mock_response.status_code = status_code

        if status_code != 200:
            mock_response.raise_for_status.side_effect = \
                (Exception(f"HTTP {status_code}"))

        mock_session = mocker.MagicMock()
        mock_session.get.return_value = mock_response
        return mock_session

    return factory


def test_get_returns(make_mock_session: Callable[int, str]) -> None:
    session = make_mock_session(status_code=200, text=MOCK_HTML)
    scraper = Scraper(session=session)

    assert scraper.get("http://example.com") == MOCK_HTML


def test_get_raises(make_mock_session: Callable[int, str]) -> None:
    session = make_mock_session(status_code=400)
    scraper = Scraper(session=session)

    with pytest.raises(Exception) as e:
        scraper.get("http://example.com")
        assert e.value.args[0] == "HTTP 400"