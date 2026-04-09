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


@pytest.mark.parametrize("html_table", [HTML_ONE_ROW_TABLE, HTML_TWO_ROW_TABLE])
def test_extract_last_id(html_table) -> None:
    assert wdumps_scraper.parsing.extract_last_id(html_table) == 5446
