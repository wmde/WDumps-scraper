import pytest

import wdumps_scraper.rendering

JSON_SPEC_INCLUDES_ALL = {
    "languages": ["de", "en"],
    "labels": True,
    "descriptions": True,
    "aliases": True,
    "sitelinks": True,
}
JSON_SPEC_NO_LABELS = {
    "descriptions": True,
    "aliases": True,
    "sitelinks": True,
}
JSON_SPEC_EXCLUDES_LABELS = {
    "labels": False,
    "descriptions": True,
    "aliases": True,
    "sitelinks": True,
}
JSON_SPEC_NO_LANGUAGES = {
    "labels": True,
    "descriptions": True,
    "aliases": True,
    "sitelinks": True,
}


def test_render_includes_all() -> None:
    assert (
        wdumps_scraper.rendering.render_includes(JSON_SPEC_INCLUDES_ALL)
        == "labels, descriptions, aliases, sitelinks"
    )


@pytest.mark.parametrize("json_spec", [JSON_SPEC_NO_LABELS, JSON_SPEC_EXCLUDES_LABELS])
def test_render_includes_no_labels(json_spec) -> None:
    assert (
        wdumps_scraper.rendering.render_includes(json_spec)
        == "descriptions, aliases, sitelinks"
    )


def test_render_languages_all() -> None:
    assert wdumps_scraper.rendering.render_languages(JSON_SPEC_INCLUDES_ALL) == "de, en"


def test_render_languages_none() -> None:
    assert wdumps_scraper.rendering.render_languages(JSON_SPEC_NO_LANGUAGES) == ""
