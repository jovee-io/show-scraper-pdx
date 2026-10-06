"""Reads data/shows.json and writes a single static index.html page, grouped
by day. Run as a module: `python -m scraper.render`
"""
import json
from datetime import date, datetime
from html import escape
from itertools import groupby
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "shows.json"
OUTPUT_PATH = ROOT / "index.html"

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Portland Shows</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>Portland Shows</h1>
<p class="sub">upcoming shows, aggregated from venue calendars around town</p>
{days}
<p class="footer">updated automatically &middot; est. 2026</p>
</body>
</html>
"""


def render_day(day: date, shows) -> str:
    heading = day.strftime("%A, %B %-d")
    items = "\n".join(
        f'  <li><a href="{escape(s["url"])}">{escape(s["venue"])} &mdash; {escape(s["title"])}</a></li>'
        for s in shows
    )
    return f"<h2>{heading}</h2>\n<ul>\n{items}\n</ul>"


def main() -> None:
    shows = json.loads(DATA_PATH.read_text()) if DATA_PATH.exists() else []
    days_html = []
    for date_str, group in groupby(shows, key=lambda s: s["date"]):
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
        days_html.append(render_day(day, list(group)))

    if not days_html:
        days_html.append("<p>No shows found. Check back soon.</p>")

    OUTPUT_PATH.write_text(PAGE_TEMPLATE.format(days="\n".join(days_html)))


if __name__ == "__main__":
    main()
