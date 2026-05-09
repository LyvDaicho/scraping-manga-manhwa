from tracker.scrapers.manga.base import MangaSiteAdapter
from tracker.scrapers.manga.fmteam_adapter import FmteamAdapter
from tracker.scrapers.manga.lelmanga_adapter import LelmangaAdapter
from tracker.scrapers.manhwa.raijin_adapter import RaijinAdapter
from tracker.scrapers.manga.anime_sama_adapter import AnimeSamaAdapter
from tracker.scrapers.manga.scan_manga_adapter import ScanMangaAdapter


ADAPTERS = {
    "lelmanga": LelmangaAdapter,
    "fmteam": FmteamAdapter,
    "raijin": RaijinAdapter,
    "anime-sama": AnimeSamaAdapter,
    "scan-manga": ScanMangaAdapter,
}


def build_manga_adapter(site_config: dict) -> MangaSiteAdapter:
    site_name = site_config["name"]
    adapter_class = ADAPTERS.get(site_name)

    if adapter_class is None:
        raise ValueError(f"Aucun adapter disponible pour le site : {site_name}")

    # Cas particuliers avec paramètres
    if site_name == "raijin":
        return adapter_class(
            base_url="https://raijin-scans.fr",
            chapter_selector=site_config["chapter_selector"],
        )

    if site_name == "anime-sama":
        return adapter_class(
            chapter_selector=site_config["chapter_selector"],
            language=site_config.get("language", "vf"),
        )

    if site_name == "scan-manga":
        # Pas de paramètres spécifiques pour l'instant
        return adapter_class()

    # Cas générique (lelmanga, fmteam, etc.)
    return adapter_class(chapter_selector=site_config["chapter_selector"])