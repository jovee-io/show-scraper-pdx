"""The Get Down PDX (Webflow) embeds a full schema.org Event as JSON-LD in
each calendar card, which is cleaner to read than the display markup.
"""
import json
from datetime import datetime

from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show

VENUE = "The Get Down PDX"
URL = "https://thegetdownpdx.com/calendar"


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select(".ca-info"):
        script = card.select_one('script[type="application/ld+json"]')
        if not script:
            continue
        try:
            event = json.loads(script.get_text())
        except json.JSONDecodeError:
            continue
        name = event.get("name")
        start_date = event.get("startDate")
        url = event.get("offers", {}).get("url")
        if not (name and start_date and url):
            continue
        try:
            date = datetime.strptime(start_date, "%b %d, %Y").date().isoformat()
        except ValueError:
            continue
        results.append(Show(venue=VENUE, title=name, date=date, url=url))
    return results
