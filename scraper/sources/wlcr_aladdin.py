"""Aladdin Theater uses a WLCR theme variant with Schema.org microdata,
which is more robust to parse than the plain-class markup other venues use.
"""
from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show
from ._wlcr_common import COVERED_BY_OWN_SOURCE, local_date_from_doors, venue_homepage

URL = "https://aladdin-theater.com/"


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select('[itemtype="http://schema.org/Event"]'):
        venue_el = card.select_one(".event-venue")
        title_el = card.select_one('[itemprop="name"]')
        link_el = card.select_one("a.event-title-link") or card.select_one("a.event-action")
        date_el = card.select_one('meta[itemprop="startDate"]')
        if not (venue_el and title_el and link_el and date_el):
            continue
        date = local_date_from_doors(date_el["content"])
        ticket_url = link_el.get("href")
        if not (ticket_url and date):
            continue
        venue = venue_el.get_text(strip=True).strip(" -")
        if not venue or venue in COVERED_BY_OWN_SOURCE:
            continue
        results.append(Show(
            venue=venue,
            title=title_el.get_text(strip=True),
            date=date,
            url=venue_homepage(venue, ticket_url),
        ))
    return results
