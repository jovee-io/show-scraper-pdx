"""Crystal Ballroom's own site runs The Events Calendar WordPress plugin,
with a full dedicated listing -- more complete than the handful of
cross-listed Crystal Ballroom shows that sometimes appear on the WLCR-family
venue pages (see _wlcr_common.COVERED_BY_OWN_SOURCE, which suppresses those
to avoid duplicate entries). Its date has no year -- infer_year() fills
that in.
"""
from datetime import datetime

from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show, infer_year

VENUE = "Crystal Ballroom"
URL = "https://www.crystalballroompdx.com/#upcoming-events"


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select(".tribe_events"):
        title_el = card.select_one(".display-in-title")
        month_el = card.select_one(".event-list-date time.icon strong")
        day_el = card.select_one(".event-list-date time.icon span")
        link_el = card.select_one("a.details-button")
        if not (title_el and month_el and day_el and link_el and link_el.get("href")):
            continue
        try:
            md = datetime.strptime(f"{month_el.get_text(strip=True)} {day_el.get_text(strip=True)}", "%B %d")
        except ValueError:
            continue
        year = infer_year(md.month, md.day)
        results.append(Show(
            venue=VENUE,
            title=title_el.get_text(strip=True),
            date=md.replace(year=year).date().isoformat(),
            url=link_el["href"],
        ))
    return results
