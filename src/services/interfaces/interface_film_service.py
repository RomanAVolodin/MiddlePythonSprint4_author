from abc import ABC, abstractmethod
from uuid import UUID

from models.film import Film


class IFilmService(ABC):
    @abstractmethod
    async def get_by_id(self, film_id: str) -> Film | None:
        raise NotImplementedError

    @abstractmethod
    async def get_films(
        self,
        page_size: int,
        page_number: int,
        sort: str | None,
        genre: UUID | None,
        query: str | None,
    ) -> list[Film]:
        raise NotImplementedError

    @abstractmethod
    async def get_genre_name_from_es(self, genre_id: UUID) -> str | None:
        raise NotImplementedError
