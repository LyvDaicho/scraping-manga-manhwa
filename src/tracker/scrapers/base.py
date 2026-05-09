from abc import ABC, abstractmethod

from tracker.models.series import Series
from tracker.models.scrape_result import ScrapeResult


class BaseScraper(ABC):
    @abstractmethod
    def can_handle(self, series: Series) -> bool:
        pass

    @abstractmethod
    def scrape(self, series: Series) -> ScrapeResult:
        pass