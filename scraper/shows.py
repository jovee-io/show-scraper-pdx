from dataclasses import dataclass, asdict
from datetime import date, timedelta


@dataclass(frozen=True)
class Show:
    venue: str
    title: str
    date: str  # ISO format YYYY-MM-DD
    url: str
    time: str = ""


def dedupe(shows: list[Show]) -> list[Show]:
    seen = set()
    result = []
    for show in shows:
        key = (show.venue, show.title, show.date, show.url)
        if key not in seen:
            seen.add(key)
            result.append(show)
    return result


def within_window(shows: list[Show], days_ahead: int = 45) -> list[Show]:
    today = date.today().isoformat()
    cutoff = (date.today() + timedelta(days=days_ahead)).isoformat()
    return [s for s in shows if today <= s.date <= cutoff]


def sort_shows(shows: list[Show]) -> list[Show]:
    return sorted(shows, key=lambda s: (s.date, s.venue, s.title))


def infer_year(month: int, day: int, today: date | None = None) -> int:
    """Pick a year for a month/day that's given without one, on the
    assumption the date is an upcoming show: if that date already fell more
    than 60 days ago this year, it must mean next year instead."""
    today = today or date.today()
    candidate = date(today.year, month, day)
    if (today - candidate).days > 60:
        return today.year + 1
    return today.year


def to_json_ready(shows: list[Show]) -> list[dict]:
    return [asdict(s) for s in shows]
