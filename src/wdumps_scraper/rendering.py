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
