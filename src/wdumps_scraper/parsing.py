from bs4 import BeautifulSoup


def extract_last_id(html_content: str) -> int:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    a_tag = table.find("a") if table else None
    href = str(a_tag["href"]) if a_tag else None
    dump_id = href.split("/")[-1] if href else None
    return int(dump_id)  # type: ignore[arg-type]
