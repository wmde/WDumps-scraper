# Scraping WDumps data
<a href="https://colab.research.google.com/github/wmde/WDumps-scraper/blob/main/notebook.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

In order to better understand what kinds of entity data dump subsets our users are interested in, this repository scrapes all dump subsets listed under "recent dumps". The scrape includes a JSON representation of the filters that were used to generate the dump.

The notebook generates a csv file that includes filter data in a human-readable form. Each row of the csv includes the following columns:
- dump name
- URL
- filter (in human-readable form including labels for any items and properties used)
- statements included in the dump (in human-readable form)
- labels (yes/no)
- descriptions (yes/no)
- aliases (yes/no)
- sitelinks (yes/no)
- languages

## Development
### Install Dependencies for Package
```
pip install -e ".[dev]"
```
