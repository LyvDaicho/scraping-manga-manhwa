from dataclasses import dataclass
from typing import Optional


@dataclass
class ScrapeResult:
    title: str
    success: bool
    site: str
    media_type: str
    current_value: Optional[int] = None
    last_update: Optional[str] = None
    error: Optional[str] = None