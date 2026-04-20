import re
from typing import Any


def render_includes(spec: dict[str, Any]) -> str:
    filters = ["labels", "descriptions", "aliases", "sitelinks"]
    dump_filters = [f for f in filters if f in spec and spec[f]]
    return ", ".join(dump_filters)


def render_languages(spec: dict[str, Any]) -> str:
    dump_languages = spec.get("languages")
    return ", ".join(dump_languages) if dump_languages else ""


def render_statement_filters(spec: dict[str, Any]) -> str:
    statements = spec.get("statements")
    return (
        "\n".join(_render_statement_filter(s) for s in statements) if statements else ""
    )


def _render_statement_filter(statement_filter: dict[str, Any]) -> str:
    simple = "simple" if statement_filter.get("simple") else ""
    rank = statement_filter["rank"].replace("-", " ")
    property_ids = statement_filter.get("properties") or []
    properties = ", ".join(property_ids) if property_ids else "all properties"
    flags = [k for k in ("qualifiers", "references") if statement_filter[k]]
    mode = "with " + " and ".join(flags) if flags else ""
    return " ".join(filter(None, [simple, rank, "statements", mode, "for", properties]))


def render_entity_filters(spec: dict[str, Any]) -> str:
    return "\n".join(_render_entity_filter(e) for e in spec["entities"])


def _render_entity_filter(entity_filter: dict[str, Any]) -> str:
    entity_type = (
        "Items where"
        if entity_filter["type"] == "item"
        else "Properties where"
        if entity_filter["type"] == "property"
        else ""
    )
    values = ", ".join(
        _render_value_constraints(p) for p in entity_filter["properties"]
    )
    return " ".join(filter(None, [entity_type, values]))


def _render_value_constraints(property_filter: dict[str, Any]) -> str:
    property_id = property_filter.get("property") or "any property"
    value_id = property_filter.get("value") or ""
    value = (
        f"is {value_id}"
        if bool(value_id) and re.match("^Q|^P", value_id)
        else "has any value"
        if not bool(value_id)
        else f"is '{value_id}'"
    )
    rank = property_filter["rank"].replace("-", " ")
    return " ".join([property_id, value, f"({rank})"])
