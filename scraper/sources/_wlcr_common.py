"""Shared helpers for the WLCR/Etix-family venue sites (Mississippi Studios,
Revolution Hall, Aladdin Theater). Each card carries a data-event-doors ISO
timestamp (UTC), which is the most reliable date source since some sites
show relative text like "Today" instead of an absolute date.

None of these venues' own sites have a per-show page -- their cards link
straight to Etix. By design, this project links to the venue's own page
rather than a ticket vendor, so we substitute the venue's homepage here
instead of the ticket link (loses per-show specificity, keeps this an
aggregator rather than a ticket funnel).
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from ..shows import Show

PACIFIC = ZoneInfo("America/Los_Angeles")

VENUE_HOMEPAGES = {
    "Mississippi Studios": "https://mississippistudios.com/",
    "Polaris Hall": "https://polarishall.com/",
    "Revolution Hall": "https://revolutionhall.com/",
    "Show Bar": "https://revolutionhall.com/",
    "Aladdin Theater": "https://aladdin-theater.com/",
    "Crystal Ballroom": "https://crystalballroompdx.com/",
}

# Venues that occasionally show up cross-listed on a WLCR-family page but
# have their own dedicated, more complete source elsewhere (see sources/
# crystal.py). Their cross-listed titles/urls don't match the dedicated
# source closely enough for dedupe() to catch, so skip them here instead.
COVERED_BY_OWN_SOURCE = {"Crystal Ballroom"}


def local_date_from_doors(doors_iso: str) -> str | None:
    try:
        dt = datetime.fromisoformat(doors_iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.astimezone(PACIFIC).date().isoformat()


def venue_name_from_logo_alt(card) -> str | None:
    logo = card.select_one(".venue-logo, .venue-logo-image")
    if not logo or not logo.get("alt"):
        return None
    alt = logo["alt"]
    for suffix in (" Logo", " logo"):
        if alt.endswith(suffix):
            alt = alt[: -len(suffix)]
            break
    return alt.strip(" -") or None


def venue_homepage(venue: str, fallback_url: str) -> str:
    """Venue's own homepage if known, else the original (ticket vendor) link
    as a last resort so an unmapped cross-listed venue still gets a working URL."""
    return VENUE_HOMEPAGES.get(venue, fallback_url)
