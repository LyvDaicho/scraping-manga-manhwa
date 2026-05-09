import re
import unicodedata


def slugify_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_text).strip().lower()
    return re.sub(r"[-\s]+", "-", cleaned)