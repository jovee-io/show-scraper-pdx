"""Star Theater runs the TicketWeb "tm-event" calendar plugin."""
from datetime import datetime
from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show

VENUES = [
    ("Star Theater", "https://startheaterportland.com/calendar/"),
    ("Jack London Revue", "https://www.jacklondonrevue.com/calendar/"),
]


def _parse_popup(popup, venue: str) -> Show | None:
    name_el = popup.select_one(".tw-name a")
    date_el = popup.select_one(".tw-event-date")
    if not (name_el and date_el and name_el.get("href")):
        return None
    try:
        dt = datetime.strptime(date_el.get_text(strip=True), "%B %d, %Y")
    except ValueError:
        return None
    return Show(
        venue=venue,
        title=name_el.get_text(strip=True),
        date=dt.date().isoformat(),
        url=name_el["href"],
    )


def get_shows() -> list[Show]:
    results = []
    for venue, url in VENUES:
        resp = get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        for popup in soup.select('[id^="tw-event-dialog-"]'):
            show = _parse_popup(popup, venue)
            if show:
                results.append(show)
    return results
