from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from tracker.scrapers.manga.base import MangaSiteAdapter


class ScanMangaAdapter(MangaSiteAdapter):
    BASE_URL = "https://www.scan-manga.com"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            "Referer": f"{self.BASE_URL}/",
            "Connection": "keep-alive",
        })

    def build_url(self, title: str) -> str:
        return self.search_url(title)

    def search_url(self, title: str) -> str:
        raise NotImplementedError(
            "La recherche Scan-Manga n'est pas encore implémentée."
        )

    def extract_latest_chapter(self, html: str, title: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        labels = [
            li.get_text(" ", strip=True)
            for li in soup.select("div.contenu_titres_fiche_technique li")
        ]
        values = [
            li.get_text(" ", strip=True)
            for li in soup.select("div.contenu_texte_fiche_technique li")
        ]

        try:
            index = next(
                i for i, label in enumerate(labels)
                if "dernier chapitre" in label.lower()
            )
        except StopIteration as exc:
            raise ValueError("Libellé 'Dernier chapitre' introuvable") from exc

        if index >= len(values):
            raise ValueError("Valeur du dernier chapitre introuvable")

        text = values[index]

        match = re.search(
            r"(?:ch|chapitre)\s*(\d+(?:\.\d+)?)",
            text,
            flags=re.IGNORECASE,
        )
        if not match:
            match = re.search(r"(\d+(?:\.\d+)?)", text)

        if not match:
            raise ValueError(
                f"Impossible d'extraire un numéro de chapitre depuis '{text}'"
            )

        return match.group(1)