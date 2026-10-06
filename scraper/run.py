"""Scrapes all venue sources, merges/dedupes/windows the results, and writes
data/shows.json. Run as a module: `python -m scraper.run`
"""
import json
import sys
from pathlib import Path

from .shows import dedupe, sort_shows, to_json_ready, within_window
from .sources import ALL_SOURCES

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "shows.json"


def main() -> None:
    all_shows = []
    for source in ALL_SOURCES:
        try:
            shows = source.get_shows()
            print(f"{source.__name__}: {len(shows)} shows", file=sys.stderr)
            all_shows.extend(shows)
        except Exception as exc:  # one venue breaking shouldn't kill the run
            print(f"{source.__name__}: FAILED - {exc}", file=sys.stderr)

    all_shows = sort_shows(within_window(dedupe(all_shows)))
    DATA_PATH.parent.mkdir(exist_ok=True)
    DATA_PATH.write_text(json.dumps(to_json_ready(all_shows), indent=2))
    print(f"wrote {len(all_shows)} shows to {DATA_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
