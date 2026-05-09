import os

import requests

from tracker.exceptions.scrape_errors import FetchError


class HttpFetcher:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def fetch_text(self, url: str) -> str:
        timeout = int(os.getenv("REQUEST_TIMEOUT", "15"))

        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            raise FetchError(f"Impossible de récupérer {url}: {exc}") from exc