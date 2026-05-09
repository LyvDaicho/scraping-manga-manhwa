from tracker.scrapers.manga.base import MangaSiteAdapter
from tracker.scrapers.manga.lelmanga_parser import extract_latest_chapter_from_html_content
from tracker.utils.slug import slugify_title

class LelmangaAdapter(MangaSiteAdapter):
    def __init__(self, chapter_selector: str) -> None:
        self.chapter_selector = chapter_selector

    def build_url(self, title: str) -> str:
        slug = slugify_title(title)
        return f"https://www.lelmanga.com/category/{slug}/"

    def extract_latest_chapter(self, html: str, title: str) -> str:
        return extract_latest_chapter_from_html_content(
            html,
            self.chapter_selector,
            title,
        )