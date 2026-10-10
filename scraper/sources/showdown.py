"""The Showdown runs the same TicketWeb "tm-event" plugin as Star Theater
and Jack London Revue (see tm_event.py), but in its "list" layout rather
than the calendar-popup layout, and its date has no year -- infer_year()
fills that in.
"""
from datetime import datetime

from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show, infer_year

VENUE = "The Showdown"
URL = "https://www.showdownpdx.com/"


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select(".tw-section"):
        title_el = card.select_one(".tw-name a")
        date_el = card.select_one(".tw-event-date")
        if not (title_el and date_el and title_el.get("href")):
            continue
        try:
            md = datetime.strptime(date_el.get_text(strip=True), "%b %d")
        except ValueError:
            continue
        year = infer_year(md.month, md.day)
        results.append(Show(
            venue=VENUE,
            title=title_el.get_text(strip=True),
            date=md.replace(year=year).date().isoformat(),
            url=title_el["href"],
        ))
    return results
