import re

from bs4 import BeautifulSoup

from tracker.scrapers.manga.base import MangaSiteAdapter
from tracker.utils.slug import slugify_title


class AnimeSamaAdapter(MangaSiteAdapter):
    def __init__(self, chapter_selector: str, language: str = "vf") -> None:
        self.chapter_selector = chapter_selector
        self.language = language

    def build_url(self, title: str) -> str:
        slug = slugify_title(title)
        return f"https://anime-sama.to/catalogue/{slug}/scan/{self.language}/"

    def extract_latest_chapter(self, html: str, title: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        options = soup.select(self.chapter_selector)

        if not options:
            raise ValueError("Aucune option de chapitre trouvée avec le sélecteur fourni")

        chapters = []
        for option in options:
            text = option.get_text(" ", strip=True)
            match = re.search(r"Chapitre\s+(\d+(?:\.\d+)?)", text, flags=re.IGNORECASE)
            if match:
                chapters.append(match.group(1))

        if not chapters:
            raise ValueError("Impossible d'extraire un numéro de chapitre depuis les options")

        return chapters[-1]