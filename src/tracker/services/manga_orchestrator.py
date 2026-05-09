from pathlib import Path
import yaml

from tracker.services.manga_orchestrator import run_manga_update
from tracker.notifiers.discord_webhook import send_discord_notification


SEPARATOR = "-" * 50
SUMMARY_SEPARATOR = "=" * 50

# Racine du projet : repo/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"

# Fichier des séries
DATA_FILE_PATH = DATA_DIR / "manga" / "manga_series.yaml"

# Fichiers de config des sites
lelmanga_cfg = CONFIG_DIR / "sites" / "manga" / "lelmanga.yaml"
scan_manga_cfg = CONFIG_DIR / "sites" / "scans" / "scan-manga.yaml"
fmteam_cfg = CONFIG_DIR / "sites" / "manga" / "fmteam.yaml"
raijin_cfg = CONFIG_DIR / "sites" / "manhwa" / "raijin.yaml"


def safe(value) -> str:
    return "-" if value is None else str(value)


def print_result(result) -> None:
    print(SEPARATOR)
    print(f"Site : {safe(result.site)}")
    print(f"Titre : {result.title}")
    print(f"Statut : {result.status}")
    print(f"Dernier chapitre : {safe(result.latest_chapter)}")
    print(f"Message : {safe(result.message)}")

    if result.status == "updated":
        send_discord_notification(
            title=result.title,
            chapters=result.latest_chapter,
            url=result.url or "-",
            site=result.site or "-",
        )


def print_summary(results: list) -> None:
    total = len(results)
    updated = sum(1 for r in results if r.status == "updated")
    unchanged = sum(1 for r in results if r.status == "unchanged")
    failed = sum(1 for r in results if r.status == "failed")

    print(SUMMARY_SEPARATOR)
    print("Récapitulatif")
    print(f"Total : {total}")
    print(f"Updated : {updated}")
    print(f"Unchanged : {unchanged}")
    print(f"Failed : {failed}")


def load_titles(data_file_path: Path) -> list[str]:
    with data_file_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    series_list = data.get("series", [])
    return [item["title"] for item in series_list if "title" in item]


def main() -> None:
    titles = load_titles(DATA_FILE_PATH)

    results = [
        run_manga_update(
            title=title,
            data_file_path=str(DATA_FILE_PATH),
            use_network=True,
        )
        for title in titles
    ]

    for result in results:
        print_result(result)

    print_summary(results)


if __name__ == "__main__":
    main()