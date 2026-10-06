"""Shared helpers for the WLCR/Etix-family venue sites (Mississippi Studios,
Revolution Hall). Each card carries a data-event-doors ISO timestamp (UTC),
which is the most reliable date source since some sites show relative text
like "Today" instead of an absolute date.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from ..shows import Show

PACIFIC = ZoneInfo("America/Los_Angeles")


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
