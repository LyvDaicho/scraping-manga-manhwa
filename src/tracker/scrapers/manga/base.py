from abc import ABC, abstractmethod


class MangaSiteAdapter(ABC):
    def build_url(self, title: str) -> str:
        return self.search_url(title)

    def search_url(self, title: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def extract_latest_chapter(self, html: str, title: str) -> str:
        raise NotImplementedError