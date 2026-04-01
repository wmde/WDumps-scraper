import json

from bs4 import BeautifulSoup


def extract_last_id(html_content: str) -> int:
  soup = BeautifulSoup(html_content, "html.parser")
  link_elem = soup.find("table").find("a")
  link_url = link_elem["href"]
  return int(link_url.split("/")[-1])

def extract_name(html_content: str) -> str:
  soup = BeautifulSoup(html_content, "html.parser")
  dump_header = soup.find("h2")
  if dump_header is not None:
    name = dump_header.text.split(": ", maxsplit=1)[-1]
    return name
  else:
    return ""

def extract_filters(html_content: str) -> dict:
  soup = BeautifulSoup(html_content, "html.parser")
  spec = soup.find("h2", string="Spec").find_next("pre").get_text()
  if spec is not None:
    dump_filters = json.loads(spec)
    return {
        "labels": "yes" if dump_filters["labels"] else "no",
        "descriptions": "yes" if dump_filters["descriptions"] else "no",
        "aliases": "yes" if dump_filters["aliases"] else "no",
        "sitelinks": "yes" if dump_filters["sitelinks"] else "no"
    }
  else:
      return {}
