def filter_series_by_site(series_list: list[dict], site_name: str) -> list[dict]:
    return [series for series in series_list if series.get("site") == site_name]