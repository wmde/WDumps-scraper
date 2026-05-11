import re
from typing import Any


def render_includes(spec: dict[str, Any]) -> str:
    filters = ["labels", "descriptions", "aliases", "sitelinks"]
    dump_filters = [f for f in filters if f in spec and spec[f]]
    return ", ".join(dump_filters)


def render_languages(spec: dict[str, Any]) -> str:
    dump_languages = spec.get("languages")
    return ", ".join(dump_languages) if dump_languages else ""


def render_statement_filters(spec: dict[str, Any], labels: dict[str, str]) -> str:
    statements = spec.get("statements")
    return (
        "\n".join(_render_statement_filter(s, labels) for s in statements)
        if statements
        else ""
    )


def _render_statement_filter(
    statement_filter: dict[str, Any], labels: dict[str, str]
) -> str:
    simple = "simple" if statement_filter.get("simple") else ""
    rank = statement_filter["rank"].replace("-", " ")
    property_ids = [
        pid
        for pid in statement_filter.get("properties") or []
        # Match against a property id pattern, as wdumper seems to allow
        # arbitrary strings
        if re.match(r"^P\d+$", pid)
    ]
    properties = (
        ", ".join(
            [f"{labels[pid]} ({pid})" if pid in labels else pid for pid in property_ids]
        )
        if property_ids
        else "all properties"
    )
    flags = [k for k in ("qualifiers", "references") if statement_filter[k]]
    mode = "with " + " and ".join(flags) if flags else ""
    return " ".join(filter(None, [simple, rank, "statements", mode, "for", properties]))


def render_entity_filters(spec: dict[str, Any], labels: dict[str, str]) -> str:
    entities = spec.get("entities")
    return (
        "\n".join(_render_entity_filter(e, labels) for e in entities)
        if entities
        else ""
    )


def _render_entity_filter(entity_filter: dict[str, Any], labels: dict[str, str]) -> str:
    entity_type = "Items" if entity_filter["type"] == "item" else "Properties"
    properties = entity_filter.get("properties") or []
    values = ", ".join(_render_value_constraints(p, labels) for p in properties)
    return f"{entity_type} where {values}"


def _render_value_constraints(
    property_filter: dict[str, Any], labels: dict[str, str]
) -> str:
    property_id = property_filter.get("property") or ""
    p = (
        f"{labels[property_id.capitalize()]} ({property_id.capitalize()})"
        if labels and property_id.capitalize() in labels
        else property_id.capitalize()
        if re.match(r"^P\d+$", property_id, re.IGNORECASE)
        else f"'{property_id}'"
        if property_id
        else "any property"
    )
    value_id = property_filter.get("value") or ""
    entity_value = True if property_filter.get("type") == "entityid" else False
    value = (
        f"is {labels[value_id.capitalize()]} ({value_id.capitalize()})"
        if labels and value_id.capitalize() in labels
        else f"is {value_id.capitalize()}"
        if re.match(r"^[Q|P]\d+$", value_id, re.IGNORECASE)
        else f"is '{value_id}'"
        if value_id
        else "has any entity value"
        if entity_value
        else "has any value"
    )
    rank = property_filter["rank"].replace("-", " ")
    return f"{p} {value} ({rank})"
