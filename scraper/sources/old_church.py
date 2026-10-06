"""The Old Church exposes a genuine public iCal feed via Tockify -- no
scraping needed at all. Note this feed includes all event types (concerts,
rentals, lectures), not only music shows; left unfiltered for simplicity.
"""
from icalendar import Calendar
from zoneinfo import ZoneInfo

from ..http import get
from ..shows import Show

FEED_URL = "https://tockify.com/api/feeds/ics/theoldchurch"
VENUE = "The Old Church"
PACIFIC = ZoneInfo("America/Los_Angeles")


def get_shows() -> list[Show]:
    resp = get(FEED_URL)
    cal = Calendar.from_ical(resp.content)
    results = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        summary = component.get("SUMMARY")
        dtstart = component.get("DTSTART")
        url = component.get("URL")
        if not (summary and dtstart and url):
            continue
        dt = dtstart.dt
        local_date = dt.astimezone(PACIFIC).date() if hasattr(dt, "astimezone") else dt
        results.append(Show(
            venue=VENUE,
            title=str(summary).strip(),
            date=local_date.isoformat(),
            url=str(url),
        ))
    return results
