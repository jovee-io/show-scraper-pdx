"""The 1905's own site is just a brochure page (events live on a separate
Wix site with no listing of its own) -- actual show data is hosted on a
third-party ticketing platform, turntabletickets.com. Its /events listing
page is a JS-rendered shell, but the sitemap lists every individual show
page directly (with the date baked into the URL), and each show page is
plain server-rendered HTML -- so: read the sitemap for URLs, scrape each
show page for its title. Still link to the venue's own homepage rather
than the ticketing platform, consistent with the rest of this project.
"""
import re
from bs4 import BeautifulSoup

from ..http import get
from ..shows import Show

VENUE = "The 1905"
VENUE_HOMEPAGE = "https://www.the1905jazz.club/"
SITEMAP_URL = "https://the1905.turntabletickets.com/sitemap.xml"
SHOW_URL_RE = re.compile(r"/shows/\d+/(\d{4}-\d{2}-\d{2})$")


def get_shows() -> list[Show]:
    sitemap_resp = get(SITEMAP_URL)
    soup = BeautifulSoup(sitemap_resp.text, "xml")
    show_urls = []
    for loc in soup.find_all("loc"):
        ticket_url = loc.get_text(strip=True)
        match = SHOW_URL_RE.search(ticket_url)
        if match:
            show_urls.append((ticket_url, match.group(1)))

    results = []
    for ticket_url, date in show_urls:
        resp = get(ticket_url)
        page = BeautifulSoup(resp.text, "lxml")
        h1 = page.find("h1")
        if not h1:
            continue
        results.append(Show(venue=VENUE, title=h1.get_text(strip=True), date=date, url=VENUE_HOMEPAGE))
    return results
