from decimal import Decimal
from typing import Any


def normalize_chapter(value: Any) -> str:
    return str(value).strip()


def chapter_to_decimal(value: str) -> Decimal:
    return Decimal(normalize_chapter(value))