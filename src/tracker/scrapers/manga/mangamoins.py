import os
import requests
from bs4 import BeautifulSoup

from tracker.models.series import Series
from tracker.models.scrape_result import ScrapeResult
from tracker.scrapers.base import BaseScraper


class MangaMoinsScraper(BaseScraper):
    SITE_NAME = "mangamoins"

    def can_handle(self, series: Series) -> bool:
        return series.site == self.SITE_NAME and series.media_type == "manga"

    def scrape(self, series: Series) -> ScrapeResult:
        timeout = int(os.getenv("REQUEST_TIMEOUT", "15"))
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            response = requests.get(series.url, headers=headers, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            chapters = soup.select("a.manga-detail__chapter")

            if not chapters:
                return ScrapeResult(
                    title=series.title,
                    success=False,
                    site=series.site,
                    media_type=series.media_type,
                    error="Aucun chapitre trouvé avec le sélecteur CSS",
                )

            return ScrapeResult(
                title=series.title,
                success=True,
                site=series.site,
                media_type=series.media_type,
                current_value=len(chapters),
            )

        except Exception as exc:
            return ScrapeResult(
                title=series.title,
                success=False,
                site=series.site,
                media_type=series.media_type,
                error=str(exc),
            )