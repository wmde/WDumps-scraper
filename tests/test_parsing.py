import pytest

import wdumps_scraper.parsing

HTML_ONE_ROW_TABLE = """
<table>
<tr>
<td><a href="/dump/5446">english lang companies</a></td>
</tr>
</table>
"""
HTML_TWO_ROW_TABLE = """
<table>
<tr>
<td><a href="/dump/5446">english lang companies</a></td>
</tr>
<tr>
<td><a href="/dump/5445">Humans</a></td>
</tr>
</table>
"""
HTML_HEADLINE = "<h2>Dump #5402: mythical-humanoid</h2>"
HTML_PREFORMATTED_TEXT = """
<h2>Spec</h2>
<p>
<code>
<pre>{
  "sitelinks" : false,
  "labels" : true,
  "descriptions" : false,
  "aliases" : false
}</pre>
</code>
</p>
"""

@pytest.mark.parametrize("html_table", [HTML_ONE_ROW_TABLE, HTML_TWO_ROW_TABLE])
def test_extract_last_id(html_table) -> int:
    assert wdumps_scraper.parsing.extract_last_id(html_table) == 5446

def test_extract_name() -> str:
    assert wdumps_scraper.parsing.extract_name(HTML_HEADLINE) == "mythical-humanoid"

def test_extract_filters() -> dict:
    assert wdumps_scraper.parsing.extract_filters(HTML_PREFORMATTED_TEXT) == {
        "labels": "yes",
        "descriptions": "no",
        "aliases": "no",
        "sitelinks": "no"
    }