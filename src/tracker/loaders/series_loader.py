from pathlib import Path
import yaml

from tracker.models.series import Series


def load_series(file_path: str) -> list[Series]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    series_items = data.get("series", [])
    result = []

    for item in series_items:
        result.append(
            Series(
                title=item["title"],
                media_type=item["media_type"],
                status=item["status"],
                site=item["site"],
                url=item["url"],
                last_chapter=item.get("last_chapter"),
                last_episode=item.get("last_episode"),
                last_update=item.get("last_update"),
            )
        )

    return result