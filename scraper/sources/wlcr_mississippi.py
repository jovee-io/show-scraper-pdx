"""Mississippi Studios' homepage also embeds Polaris Hall's shows on the same
page (distinguished by data-venue-id / venue logo), so one fetch covers both.
"""
from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show
from ._wlcr_common import local_date_from_doors, venue_name_from_logo_alt

URL = "https://mississippistudios.com/"


def get_shows() -> list[Show]:
    resp = get(URL)
    soup = BeautifulSoup(resp.text, "lxml")
    results = []
    for card in soup.select("[data-venue-id]"):
        venue = venue_name_from_logo_alt(card)
        title_el = card.select_one(".event-title a")
        doors_el = card.select_one("[data-event-doors]")
        if not (venue and title_el and doors_el):
            continue
        title = title_el.get_text(strip=True)
        url = title_el.get("href")
        date = local_date_from_doors(doors_el["data-event-doors"])
        if not (url and date):
            continue
        results.append(Show(venue=venue, title=title, date=date, url=url))
    return results
