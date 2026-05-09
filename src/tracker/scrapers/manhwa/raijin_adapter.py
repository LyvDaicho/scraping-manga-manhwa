import re

from bs4 import BeautifulSoup

from tracker.scrapers.manga.base import MangaSiteAdapter
from tracker.utils.slug import slugify_title


class RaijinAdapter(MangaSiteAdapter):
    def __init__(self, base_url: str, chapter_selector: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.chapter_selector = chapter_selector

    def build_url(self, title: str) -> str:
        slug = slugify_title(title)
        return f"{self.base_url}/manga/{slug}/"

    def extract_latest_chapter(self, html: str, title: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select(self.chapter_selector)

        if not links:
            raise ValueError("Aucun lien de chapitre trouvé avec le sélecteur fourni")

        first_link = links[0]

        title_attr = first_link.get("title") or ""
        text = first_link.get_text(" ", strip=True)
        href = first_link.get("href") or ""

        patterns = [
            r"Chapitre\s+(\d+(?:\.\d+)?)",
            r"chapter[-\s](\d+(?:\.\d+)?)",
            r"/(\d+(?:\.\d+)?)(?:/)?$",
        ]

        for source in (title_attr, text, href):
            for pattern in patterns:
                match = re.search(pattern, source, flags=re.IGNORECASE)
                if match:
                    return match.group(1)

        raise ValueError("Impossible d'extraire le numéro de chapitre")