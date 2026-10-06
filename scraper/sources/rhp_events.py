"""Doug Fir Lounge, Wonder Ballroom, Holocene, Roseland Theater -- all run the
same WordPress "RHP Events" plugin with identical markup (.rhpSingleEvent cards).
"""
from datetime import datetime
from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show

VENUES = [
    ("Doug Fir Lounge", "https://dougfirlounge.com/events/"),
    ("Wonder Ballroom", "https://wonderballroom.com/events/"),
    ("Holocene", "https://holocene.org/events/"),
    ("Roseland Theater", "https://roselandpdx.com/events/"),
]


def _parse_card(card, venue: str) -> Show | None:
    title_el = card.select_one("#eventTitle") or card.select_one(".rhp-event__title--list")
    if not title_el:
        return None
    title = title_el.get_text(strip=True)
    url_el = card.select_one("a.url")
    if not url_el or not url_el.get("href"):
        return None
    url = url_el["href"]

    date_el = card.select_one("#eventDate") or card.select_one(".eventMonth")
    if not date_el:
        return None
    date_text = date_el.get_text(strip=True)  # e.g. "Thu, Oct 01, 2026"
    try:
        dt = datetime.strptime(date_text, "%a, %b %d, %Y")
    except ValueError:
        return None

    return Show(venue=venue, title=title, date=dt.date().isoformat(), url=url)


def get_shows() -> list[Show]:
    results = []
    for venue, url in VENUES:
        resp = get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        for card in soup.select(".rhpSingleEvent"):
            show = _parse_card(card, venue)
            if show:
                results.append(show)
    return results
