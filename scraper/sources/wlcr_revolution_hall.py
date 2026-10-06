"""Revolution Hall's homepage also carries its secondary room, Show Bar,
distinguished the same way as Mississippi Studios/Polaris Hall.
"""
from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show
from ._wlcr_common import local_date_from_doors, venue_homepage, venue_name_from_logo_alt

URL = "https://revolutionhall.com/"

_VENUE_NAME_FIXUPS = {"Showbar": "Show Bar"}


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select("[data-event-id][data-venue-id]"):
        venue = venue_name_from_logo_alt(card)
        if venue:
            venue = _VENUE_NAME_FIXUPS.get(venue, venue)
        title_el = card.select_one("h3 a") or card.select_one('[itemprop="name"] a')
        doors_el = card.select_one("[data-event-doors]")
        if not (venue and title_el and doors_el):
            continue
        title = title_el.get_text(strip=True)
        ticket_url = title_el.get("href")
        date = local_date_from_doors(doors_el["data-event-doors"])
        if not (ticket_url and date):
            continue
        results.append(Show(venue=venue, title=title, date=date, url=venue_homepage(venue, ticket_url)))
    return results
