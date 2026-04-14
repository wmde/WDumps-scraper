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
    if spec["statements"]:
        statements = spec["statements"]
        statement_filters = ""
        for i in range(0, len(statements)):
            rank = (
                "best rank"
                if statements[i]["rank"] == "best-rank"
                else "all ranks"
                if statements[i]["rank"] == "all"
                else statements[i]["rank"] + " rank"
            )
            properties = (
                ""
                if "properties" not in statements[i]
                else f" for {
                    'all properties'
                    if statements[i]['properties'] is None
                    else ', '.join(statements[i]['properties'])
                    if statements[i]['properties']
                    else ''
                }"
            )
            qualifiers_references = [
                k for k in ("qualifiers", "references") if statements[i][k]
            ]
            if i > 0:
                statement_filters = statement_filters + "\n"
            statement_filters = f"{statement_filters}{rank} statements{properties}{
                ' with ' + ' and '.join(qualifiers_references)
                if qualifiers_references
                else ''
            }"
        return statement_filters
    else:
        return ""
