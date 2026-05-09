from pathlib import Path
import yaml


def load_roles(file_path: str) -> dict:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    return data.get("roles", {})