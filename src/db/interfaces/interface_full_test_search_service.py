from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class IFullTextSearchService(ABC):
    @abstractmethod
    async def search(self, index: str, body: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, index: str, id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def get_genre_name_from_es(self, genre_id: UUID) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError
