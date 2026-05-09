from dataclasses import dataclass


@dataclass
class OrchestrationResult:
    title: str
    site: str | None
    status: str
    message: str | None = None
    latest_chapter: str | None = None
    url: str | None = None