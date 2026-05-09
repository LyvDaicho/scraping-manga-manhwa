import logging
from pathlib import Path

import yaml

from tracker.models.orchestration_result import OrchestrationResult
from tracker.scrapers.manga.registry import build_manga_adapter
from tracker.services.http_fetcher import HttpFetcher
from tracker.services.manga_update_service import update_last_chapter
from tracker.utils.chapter import chapter_to_decimal


logger = logging.getLogger(__name__)


SOURCE_PRIORITY = {
    "manga": ["lelmanga", "scan-manga"],
    "manhwa": ["raijin", "scan-manga"],
}


PROJECT_ROOT = Path(__file__).resolve().parents[3]


SITE_CONFIG_PATHS = {
    "lelmanga":   PROJECT_ROOT / "config" / "sites" / "manga" / "lelmanga.yaml",
    "fmteam":     PROJECT_ROOT / "config" / "sites" / "manga" / "fmteam.yaml",
    "raijin":     PROJECT_ROOT / "config" / "sites" / "manhwa" / "raijin.yaml",
    "scan-manga": PROJECT_ROOT / "config" / "sites" / "scans" / "scan-manga.yaml",
}


SCAN_MANGA_OVERRIDES_PATH = (
    PROJECT_ROOT / "config" / "overrides" / "scan-manga.yaml"
)


def load_site_config(site_name: str) -> dict:
    config_path = SITE_CONFIG_PATHS.get(site_name)
    if config_path is None:
        raise ValueError(f"Aucun fichier de configuration défini pour le site : {site_name}")

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_scan_manga_overrides() -> dict:
    if not SCAN_MANGA_OVERRIDES_PATH.exists():
        return {}

    with SCAN_MANGA_OVERRIDES_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    return data.get("titles", {})


def run_manga_update(
    title: str,
    data_file_path: str,
    html_file_path: str | None = None,
    use_network: bool = False,
) -> OrchestrationResult:
    try:
        with open(data_file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        series_list = data.get("series", [])
        series = next((item for item in series_list if item.get("title") == title), None)

        if series is None:
            return OrchestrationResult(
                title=title,
                site=None,
                status="failed",
                message="Série introuvable dans le fichier de data",
            )

        work_type = series.get("type")
        if not work_type:
            return OrchestrationResult(
                title=title,
                site=None,
                status="failed",
                message="Le type de la série est manquant",
            )

        priority_sites = series.get("sources") or SOURCE_PRIORITY.get(work_type, [])
        if not priority_sites:
            return OrchestrationResult(
                title=title,
                site=None,
                status="failed",
                message=f"Aucune source définie pour le type : {work_type}",
            )

        scan_manga_overrides = load_scan_manga_overrides()
        fetcher = HttpFetcher()
        collected_results: list[dict] = []

        for site_name in priority_sites:
            try:
                site_config = load_site_config(site_name)
                adapter = build_manga_adapter(site_config)

                if use_network:
                    override_url = None
                    if site_name == "scan-manga":
                        override_url = scan_manga_overrides.get(title)

                    if override_url:
                        url = override_url
                    else:
                        url = adapter.build_url(title)

                    html = fetcher.fetch_text(url)
                else:
                    if html_file_path is None:
                        continue
                    with open(html_file_path, "r", encoding="utf-8") as file:
                        html = file.read()
                    url = None  # pas d'URL en mode fichier

                latest_chapter = adapter.extract_latest_chapter(html, title)

                if latest_chapter:
                    collected_results.append(
                        {
                            "site": site_name,
                            "chapter": latest_chapter,
                            "url": url,
                        }
                    )

            except Exception as exc:
                logger.warning("Échec source %s pour %s: %s", site_name, title, exc)

        if not collected_results:
            return OrchestrationResult(
                title=title,
                site=None,
                status="failed",
                message="Aucun résultat valide trouvé sur les sources testées",
            )

        best_result = max(
            collected_results,
            key=lambda item: chapter_to_decimal(item["chapter"]),
        )

        updated = update_last_chapter(data_file_path, title, best_result["chapter"])

        return OrchestrationResult(
            title=title,
            site=best_result["site"],
            status="updated" if updated else "unchanged",
            latest_chapter=best_result["chapter"],
            message="Mise à jour effectuée" if updated else "Aucun changement détecté",
            url=best_result.get("url"),
        )

    except Exception as exc:
        return OrchestrationResult(
            title=title,
            site=None,
            status="failed",
            message=str(exc),
        )