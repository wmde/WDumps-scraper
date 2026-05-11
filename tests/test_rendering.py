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
            "properties": ["P31", "P279"],
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

JSON_LABELS_MULTIPLE_EXIST = {
    "Q106": "Uranus",
    "P31": "instance of",
    "P279": "subclass of",
}
JSON_LABELS_SINGLE_EXIST = {"P31": "instance of"}
JSON_NO_LABELS: dict = {}

JSON_SPEC_ENTITIES_ITEMS_ALL = {
    "entities": [
        {
            "type": "item",
            "properties": [
                {"property": "", "rank": "all", "type": "anyvalue", "value": None}
            ],
        }
    ],
}
JSON_SPEC_ENTITIES_EMPTY: dict = {"entities": []}
JSON_SPEC_ENTITIES_NONE: dict = {}
JSON_SPEC_ENTITIES_MULTIPLE_VALUES = {
    "entities": [
        {
            "type": "item",
            "properties": [
                {
                    "property": "p31",
                    "rank": "best-rank",
                    "type": "entityid",
                    "value": None,
                },
                {
                    "property": "P279",
                    "rank": "non-deprecated",
                    "type": "entityid",
                    "value": "wd:Q901",
                },
            ],
        }
    ],
}
JSON_SPEC_ENTITIES_MULTIPLE_TYPES = {
    "entities": [
        {
            "type": "item",
            "properties": [
                {"property": "P31", "rank": "best-rank", "value": "q106"},
            ],
        },
        {
            "type": "property",
            "properties": [
                {
                    "property": "schema:isPartOf",
                    "rank": "non-deprecated",
                    "value": None,
                },
            ],
        },
    ]
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


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_statement_filters_all(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(
            JSON_SPEC_STATEMENTS_ALL, json_labels
        )
        == "all statements with qualifiers and references for all properties"
    )


def test_render_statement_filters_multiple_no_labels() -> None:
    assert wdumps_scraper.rendering.render_statement_filters(
        JSON_SPEC_STATEMENTS_MULTIPLE, JSON_NO_LABELS
    ) == (
        "non deprecated statements with qualifiers and references "
        "for all properties\n"
        "best rank statements with qualifiers for P31, P279"
    )


def test_render_statement_filters_multiple_with_labels() -> None:
    assert wdumps_scraper.rendering.render_statement_filters(
        JSON_SPEC_STATEMENTS_MULTIPLE, JSON_LABELS_MULTIPLE_EXIST
    ) == (
        "non deprecated statements with qualifiers and references "
        "for all properties\n"
        "best rank statements with qualifiers for instance of (P31), subclass of (P279)"
    )


def test_render_statement_filters_single_with_labels() -> None:
    assert wdumps_scraper.rendering.render_statement_filters(
        JSON_SPEC_STATEMENTS_MULTIPLE, JSON_LABELS_SINGLE_EXIST
    ) == (
        "non deprecated statements with qualifiers and references "
        "for all properties\n"
        "best rank statements with qualifiers for instance of (P31), P279"
    )


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_statement_filters_no_properties(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(
            JSON_SPEC_STATEMENTS_NO_PROPERTIES, json_labels
        )
        == "all statements with qualifiers and references for all properties"
    )


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_statement_filters_simple(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(
            JSON_SPEC_SIMPLE_STATEMENTS, json_labels
        )
        == "simple all statements with qualifiers and references for all properties"
    )


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_statement_filters_none(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_statement_filters(
            JSON_SPEC_STATEMENTS_NONE, json_labels
        )
        == ""
    )


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_entity_filters_items_all(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_entity_filters(
            JSON_SPEC_ENTITIES_ITEMS_ALL, json_labels
        )
        == "Items where any property has any value (all)"
    )


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_entity_filters_empty(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_entity_filters(
            JSON_SPEC_ENTITIES_EMPTY, json_labels
        )
        == ""
    )


@pytest.mark.parametrize("json_labels", [JSON_NO_LABELS, JSON_LABELS_MULTIPLE_EXIST])
def test_render_entity_filters_none(json_labels) -> None:
    assert (
        wdumps_scraper.rendering.render_entity_filters(
            JSON_SPEC_ENTITIES_NONE, json_labels
        )
        == ""
    )


def test_render_entity_filters_multiple_values_no_labels() -> None:
    assert wdumps_scraper.rendering.render_entity_filters(
        JSON_SPEC_ENTITIES_MULTIPLE_VALUES, JSON_NO_LABELS
    ) == (
        "Items where P31 has any entity value (best rank), "
        "P279 is 'wd:Q901' (non deprecated)"
    )


def test_render_entity_filters_multiple_values_single_label() -> None:
    assert wdumps_scraper.rendering.render_entity_filters(
        JSON_SPEC_ENTITIES_MULTIPLE_VALUES, JSON_LABELS_SINGLE_EXIST
    ) == (
        "Items where instance of (P31) has any entity value (best rank), "
        "P279 is 'wd:Q901' (non deprecated)"
    )


def test_render_entity_filters_multiple_types_multiple_labels() -> None:
    assert wdumps_scraper.rendering.render_entity_filters(
        JSON_SPEC_ENTITIES_MULTIPLE_TYPES, JSON_LABELS_MULTIPLE_EXIST
    ) == (
        "Items where instance of (P31) is Uranus (Q106) (best rank)\n"
        "Properties where 'schema:isPartOf' has any value (non deprecated)"
    )
