from typing import Any


def render_includes(spec: dict[str, Any]) -> str:
    filters = ["labels", "descriptions", "aliases", "sitelinks"]
    dump_filters = [filter for filter in filters if filter in spec and spec[filter]]
    return ", ".join(dump_filters)
