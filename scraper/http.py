import time
import requests

USER_AGENT = "Mozilla/5.0 (compatible; PortlandShowsBot/1.0)"

_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})


def get(url: str, delay: float = 1.0, **kwargs) -> requests.Response:
    resp = _session.get(url, timeout=20, **kwargs)
    resp.raise_for_status()
    if delay:
        time.sleep(delay)
    return resp
