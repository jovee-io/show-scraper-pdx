"""Alberta Street Pub runs Squarespace's native event list, server-rendered
with an ISO datetime attribute -- no date-format guesswork needed.
"""
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show

VENUE = "Alberta Street Pub"
BASE_URL = "https://www.albertastreetpub.com"
URL = f"{BASE_URL}/music"


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select("article.eventlist-event"):
        title_el = card.select_one(".eventlist-title-link")
        date_el = card.select_one("time.event-date")
        if not (title_el and date_el and date_el.get("datetime") and title_el.get("href")):
            continue
        results.append(Show(
            venue=VENUE,
            title=title_el.get_text(strip=True),
            date=date_el["datetime"],
            url=urljoin(BASE_URL, title_el["href"]),
        ))
    return results
