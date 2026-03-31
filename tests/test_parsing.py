import pytest
import wdumps_scraper.parsing
from wdumps_scraper import parsing

@pytest.fixture
def html_last_id():
    html = """
    <!DOCTYPE html>
<html>
<head>
<link href="//wdumps.toolforge.org/static/minireset.min.css" rel="stylesheet"/>
<link href="//wdumps.toolforge.org/static/main.css" rel="stylesheet"/>
<script defer="" type="text/javascript">
            const ICONS_URL = '//wdumps.toolforge.org/static/icons';
            const API_URL = '//wdumps.toolforge.org/';
            const ROOT = '//wdumps.toolforge.org/';
        </script>
<script defer="" src="//wdumps.toolforge.org/static/langcodes.js"></script>
<script defer="" src="//wdumps.toolforge.org/static/main.js"></script>
<title>WDumper</title>
</head>
<body>
<div class="bar">
<header>
<a href="//wdumps.toolforge.org/"><h1>WDumper</h1></a>
<p>A tool to create custom wikidata RDF dumps</p>
<div class="end">
<a href="//wdumps.toolforge.org/about">About</a>
<a href="//wdumps.toolforge.org/dumps">Recent dumps</a>
</div>
</header>
</div>
<main data-view="" id="main">
<h2>Recent dumps</h2>
<table>
<tr>
<td>Title</td>
<td>Created at</td>
<td>Finished</td>
<td>Download link</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5446">english lang companies</a></td>
<td>2026-03-31T15:02:20Z</td>
<td>
          not finished
      </td>
<td>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5445">Humans</a></td>
<td>2026-03-31T07:02:07Z</td>
<td>
          not finished
      </td>
<td>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5444">m</a></td>
<td>2026-03-31T06:19:45Z</td>
<td>
          not finished
      </td>
<td>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5443">marv</a></td>
<td>2026-03-31T06:10:27Z</td>
<td>
          at 2026-03-31T15:02:58Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5443">Download</a>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5442">All musicians and musical groups</a></td>
<td>2026-03-30T09:43:34Z</td>
<td>
          at 2026-03-30T18:39:24Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5442">Download</a>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5441">music people and groups</a></td>
<td>2026-03-29T16:31:49Z</td>
<td>
          at 2026-03-30T09:18:06Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5441">Download</a>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5440">allmusic people</a></td>
<td>2026-03-29T16:05:18Z</td>
<td>
          at 2026-03-30T00:52:00Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5440">Download</a>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5439"></a></td>
<td>2026-03-28T16:00:23Z</td>
<td>
          at 2026-03-29T00:43:21Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5439">Download</a>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5438"></a></td>
<td>2026-03-27T16:57:58Z</td>
<td>
          at 2026-03-28T01:37:34Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5438">Download</a>
</td>
</tr>
<tr>
<td><a href="//wdumps.toolforge.org/dump/5437"></a></td>
<td>2026-03-26T09:35:25Z</td>
<td>
          at 2026-03-26T18:20:52Z
      </td>
<td>
<a href="//wdumps.toolforge.org/download/5437">Download</a>
</td>
</tr>
</table>
<a class="next" href="//wdumps.toolforge.org/dumps?first=5437">Next</a>
</main>
</body>
</html>
"""
    return html

@pytest.fixture
def html_content():
    html = """
    <!DOCTYPE html>
<html>
<head>
<link href="//wdumps.toolforge.org/static/minireset.min.css" rel="stylesheet"/>
<link href="//wdumps.toolforge.org/static/main.css" rel="stylesheet"/>
<script defer="" type="text/javascript">
            const ICONS_URL = '//wdumps.toolforge.org/static/icons';
            const API_URL = '//wdumps.toolforge.org/';
            const ROOT = '//wdumps.toolforge.org/';
        </script>
<script defer="" src="//wdumps.toolforge.org/static/langcodes.js"></script>
<script defer="" src="//wdumps.toolforge.org/static/main.js"></script>
<title>WDumper</title>
</head>
<body>
<div class="bar">
<header>
<a href="//wdumps.toolforge.org/"><h1>WDumper</h1></a>
<p>A tool to create custom wikidata RDF dumps</p>
<div class="end">
<a href="//wdumps.toolforge.org/about">About</a>
<a href="//wdumps.toolforge.org/dumps">Recent dumps</a>
</div>
</header>
</div>
<main data-view="info" id="main">
<h2>Dump #5402: mythical-humanoid</h2>
<p>
</p>
<div class="intro">
<p>
<a class="link-button" href="//wdumps.toolforge.org/download/5402">
<img alt="" src="//wdumps.toolforge.org/static/icons/download.svg"/>
                download
            </a>
</p>
</div>
<p>
<h2>Info</h2>
<table>
<tr>
<td>Statement count</td>
<td>748</td>
</tr>
<tr>
<td>Entity count</td>
<td>34</td>
</tr>
<tr>
<td>Triple count</td>
<td>8067</td>
</tr>
<tr>
<td>Source dump date</td>
<td>20260223</td>
</tr>
<tr>
<td>Tool version</td>
<td><a href="https://github.com/bennofs/wdumper/commit/dc325fc0be521d4994a4cd0e90f7b4f8baf3ae6b">git-dc325fc0be</a></td>
</tr>
<tr>
<td>Wikidata-Toolkit version</td>
<td><a href="https://github.com/Wikidata/Wikidata-Toolkit/commit/0afe49fef56a6da58a8f8fd3f023a56920c04f3b">git-0afe49fef5</a></td>
</tr>
</table>
<div class="section">
<h2>Zenodo</h2>
<table>
<tr>
<td>Sandbox</td>
<td>
<button class="upload" data-dump-id="5402" data-target="sandbox">Upload to Sandbox</button>
</td>
</tr>
<tr>
<td>Main</td>
<td>
<button class="upload" data-dump-id="5402" data-target="release">Upload to Release</button>
</td>
</tr>
</table>
</div>
<div class="section">
<h2>Timings</h2>
<table>
<tr>
<td>Created at</td>
<td>2026-03-04T14:53:26Z </td>
</tr>
<tr>
<td>Processing started at</td>
<td>
                    2026-03-04T20:20:23Z
                    
                </td>
</tr>
<tr>
<td>Processing finished at</td>
<td>
                    2026-03-05T04:56:27Z
                    
                </td>
</tr>
<tr>
<td>Processed items</td>
<td>119162424 </td>
</tr>
</table>
</div>
<div class="section">
<h2>Spec</h2>
<p>
<code>
<pre>{
  "version" : "1",
  "entities" : [ {
    "type" : "item",
    "properties" : [ {
      "property" : "P31",
      "rank" : "best-rank",
      "type" : "entityid",
      "value" : "Q24533670"
    } ]
  } ],
  "samplingPercent" : 100,
  "statements" : [ {
    "properties" : null,
    "rank" : "best-rank",
    "simple" : true,
    "full" : true,
    "references" : false,
    "qualifiers" : true
  } ],
  "sitelinks" : false,
  "labels" : true,
  "descriptions" : false,
  "aliases" : false,
  "languages" : null,
  "meta" : true
}</pre>
</code>
</p>
</div>
</p></main>
</body>
</html>
"""
    return html

def test_extract_last_id(html_last_id: str) -> int:
    assert wdumps_scraper.parsing.extract_last_id(html_last_id) == 5446

def test_extract_name(html_content: str) -> str:
    assert wdumps_scraper.parsing.extract_name(html_content) == "mythical-humanoid"

def test_extract_filters(html_content: str) -> dict:
    assert wdumps_scraper.parsing.extract_filters(html_content) == {'labels': 'yes', 'descriptions': 'no', 'aliases': 'no', 'sitelinks': 'no'}