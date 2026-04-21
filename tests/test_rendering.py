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

JSON_SPEC_STATEMENTS_ALL = {
    "statements": [
        {"properties": None, "rank": "all", "references": True, "qualifiers": True}
    ]
}
JSON_SPEC_STATEMENTS_MULTIPLE = {
    "statements": [
        {
            "properties": None,
            "rank": "non-deprecated",
            "references": True,
            "qualifiers": True,
        },
        {
            "properties": ["P106", "P27"],
            "rank": "best-rank",
            "references": False,
            "qualifiers": True,
        },
    ]
}
JSON_SPEC_STATEMENTS_NO_PROPERTIES = {
    "statements": [{"rank": "all", "references": True, "qualifiers": True}]
}
JSON_SPEC_SIMPLE_STATEMENTS = {
    "statements": [
        {"rank": "all", "references": True, "qualifiers": True, "simple": True}
    ]
}
JSON_SPEC_STATEMENTS_NONE: dict = {}


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


def test_render_statement_filters_all() -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(JSON_SPEC_STATEMENTS_ALL)
        == "all statements with qualifiers and references for all properties"
    )


def test_render_statement_filters_multiple() -> None:
    assert wdumps_scraper.rendering.render_statement_filters(
        JSON_SPEC_STATEMENTS_MULTIPLE
    ) == (
        "non deprecated statements with qualifiers and references "
        "for all properties\n"
        "best rank statements with qualifiers for P106, P27"
    )


def test_render_statement_filters_no_properties() -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(
            JSON_SPEC_STATEMENTS_NO_PROPERTIES
        )
        == "all statements with qualifiers and references for all properties"
    )


def test_render_statement_filters_simple() -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(JSON_SPEC_SIMPLE_STATEMENTS)
        == "simple all statements with qualifiers and references for all properties"
    )


def test_render_statement_filters_none() -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(JSON_SPEC_STATEMENTS_NONE)
        == ""
    )
