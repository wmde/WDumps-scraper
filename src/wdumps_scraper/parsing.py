import json

from bs4 import BeautifulSoup


def extract_last_id(html_content: str) -> int:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    a_tag = table.find("a") if table else None
    href = str(a_tag["href"]) if a_tag else None
    dump_id = href.split("/")[-1] if href else None
    return int(dump_id)  # type: ignore[arg-type]


def extract_name(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    dump_header = soup.find("h2")
    if not dump_header:
        return ""
    return dump_header.text.split(": ", maxsplit=1)[-1]


def extract_filters(html_content: str) -> dict[str, str]:
    soup = BeautifulSoup(html_content, "html.parser")
    spec_tag = soup.find("h2", string="Spec")  # type: ignore[call-overload]
    if not spec_tag:
        return {}
    pre = spec_tag.find_next("pre")
    if not pre:
        return {}
    dump_filters = json.loads(pre.get_text())
    return {
        "labels": "yes" if dump_filters["labels"] else "no",
        "descriptions": "yes" if dump_filters["descriptions"] else "no",
        "aliases": "yes" if dump_filters["aliases"] else "no",
        "sitelinks": "yes" if dump_filters["sitelinks"] else "no",
    }
