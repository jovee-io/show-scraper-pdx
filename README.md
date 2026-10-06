# Portland Shows

A small static page listing upcoming shows at Portland, OR music venues, aggregated from each venue's own site.

Updated automatically once a day. No database, no JS, no tracking.

## How it works

- `scraper/sources/` has one module per venue (or group of venues sharing the same underlying platform).
- `python -m scraper.run` fetches all sources and writes `data/shows.json`.
- `python -m scraper.render` turns that into `index.html`.
- A scheduled GitHub Action runs both steps daily and commits the result.

## Local development

```
pip install -r requirements.txt
python -m scraper.run
python -m scraper.render
```

Then open `index.html` in a browser.

## Adding a venue

Add a module under `scraper/sources/` exposing `get_shows() -> list[Show]`, and
register it in `scraper/sources/__init__.py`.
