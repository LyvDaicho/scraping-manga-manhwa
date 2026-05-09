from tracker.scrapers.manga.base import MangaSiteAdapter
from tracker.utils.slug import slugify_title
import json


class FmteamAdapter(MangaSiteAdapter):
    def __init__(self, chapter_selector: str | None = None) -> None:
        self.chapter_selector = chapter_selector

    def build_url(self, title: str) -> str:
        slug = slugify_title(title)
        return f"https://fmteam.fr/api/comics/{slug}"

    def extract_latest_chapter(self, html: str, title: str) -> str:
        data = json.loads(html)
        last_chapter = data["comic"]["last_chapter"]
        return str(last_chapter["chapter"])