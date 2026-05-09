from pathlib import Path
import yaml

from tracker.utils.chapter import chapter_to_decimal, normalize_chapter


def update_last_chapter(file_path: str, title: str, new_chapter: str) -> bool:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    series_list = data.get("series", [])
    updated = False
    normalized_new = normalize_chapter(new_chapter)

    for series in series_list:
        if series.get("title") == title:
            current = normalize_chapter(series.get("last_chapter", ""))
            if chapter_to_decimal(current) != chapter_to_decimal(normalized_new):
                series["last_chapter"] = normalized_new
                updated = True

    if updated:
        with path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)

    return updated