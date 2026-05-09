from dataclasses import dataclass
from typing import Optional


@dataclass
class Series:
    title: str
    media_type: str
    status: str
    site: str
    url: str
    last_chapter: Optional[int] = None
    last_episode: Optional[int] = None
    last_update: Optional[str] = None