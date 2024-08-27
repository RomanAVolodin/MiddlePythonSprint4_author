from uuid import UUID

from models.film import Genre


class IGenreService:
    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        raise NotImplementedError

    async def get_genres(self) -> list[Genre]:
        raise NotImplementedError
