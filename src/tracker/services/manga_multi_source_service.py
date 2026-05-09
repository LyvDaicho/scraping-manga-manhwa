from dataclasses import dataclass
from datetime import date

from tracker.scrapers.manga.registry import build_manga_adapter
from tracker.utils.chapter import chapter_to_decimal


SOURCE_PRIORITY = {
    "manga": ["lelmanga", "fmteam"],
    "manwha": ["lelmanga"],
}


SITE_CONFIGS = {
    "lelmanga": {
        "name": "lelmanga",
        "chapter_selector": ".inepcx a",
    },
    "fmteam": {
        "name": "fmteam",
        "chapter_selector": ".item .chapter a.filter",
    },
}


@dataclass
class SourceResult:
    site: str
    chapter: str | None
    success: bool
    message: str | None = None


def resolve_best_source_result(title: str, work_type: str, fetch_html) -> SourceResult:
    results: list[SourceResult] = []

    for site_name in SOURCE_PRIORITY.get(work_type, []):
        site_config = SITE_CONFIGS.get(site_name)
        if not site_config:
            continue

        adapter = build_manga_adapter(site_config)

        try:
            url = adapter.build_url(title)
            html = fetch_html(url)
            chapter = adapter.extract_latest_chapter(html, title)
            results.append(SourceResult(site=site_name, chapter=chapter, success=True))
        except Exception as exc:
            results.append(SourceResult(site=site_name, chapter=None, success=False, message=str(exc)))

    valid_results = [result for result in results if result.success and result.chapter is not None]
    if not valid_results:
        raise ValueError(f"Aucun résultat valide trouvé pour {title}")

    return max(valid_results, key=lambda result: chapter_to_decimal(result.chapter))