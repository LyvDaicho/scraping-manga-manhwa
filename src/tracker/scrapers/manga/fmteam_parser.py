import re
from pathlib import Path

from bs4 import BeautifulSoup

from tracker.utils.chapter import chapter_to_decimal


def extract_latest_chapter_from_html_content(html: str, selector: str, title: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    links = soup.select(selector)
    if not links:
        raise ValueError("Aucun lien trouvé avec le sélecteur fourni.")

    chapter_values = []

    for link in links:
        text = link.get_text(strip=True)
        match = re.search(r"Chapitre\s+(\d+(?:\.\d+)?)", text, flags=re.IGNORECASE)
        if match:
            chapter_values.append(match.group(1))
            continue

        href = link.get("href", "")
        match = re.search(r"/ch/(\d+(?:\.\d+)?)", href, flags=re.IGNORECASE)
        if match:
            chapter_values.append(match.group(1))

    if not chapter_values:
        raise ValueError("Aucun numéro de chapitre détecté dans les liens.")

    return max(chapter_values, key=chapter_to_decimal)


def extract_latest_chapter_from_html(file_path: str, selector: str, title: str) -> str:
    html = Path(file_path).read_text(encoding="utf-8")
    return extract_latest_chapter_from_html_content(html, selector, title)