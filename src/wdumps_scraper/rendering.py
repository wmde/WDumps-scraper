from typing import Any


def render_includes(spec: dict[str, Any]) -> str:
    filters = ["labels", "descriptions", "aliases", "sitelinks"]
    dump_filters = [f for f in filters if f in spec and spec[f]]
    return ", ".join(dump_filters)


def render_languages(spec: dict[str, Any]) -> str:
    dump_languages = spec.get("languages")
    if dump_languages is None:
        return ""
    return ", ".join(dump_languages)


def render_statement_filters(spec: dict[str, Any]) -> str:
    return "\n".join(_render_statement_filter(s) for s in spec["statements"])


def _render_statement_filter(statement_filter: dict[str, Any]) -> str:
    simple = "simple" if statement_filter.get("simple") else ""
    rank = statement_filter["rank"].replace("-", " ")
    property_ids = statement_filter.get("properties") or []
    properties = ", ".join(property_ids) if property_ids else "all properties"
    flags = [k for k in ("qualifiers", "references") if statement_filter[k]]
    mode = "with " + " and ".join(flags) if flags else ""
    return " ".join(filter(None, [simple, rank, "statements", mode, "for", properties]))
