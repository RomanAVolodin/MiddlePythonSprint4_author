import json
import logging
from functools import lru_cache
from uuid import UUID

from core.config import GENRE_CACHE_EXPIRE_IN_SECONDS, SIZE_RESPONSE
from db.cache_service import ICacheService, get_cache_service
from db.full_text_search_service import IFullTextSearchService, get_full_text_search
from elasticsearch import NotFoundError
from models.film import CustomJSONEncoder, Genre
from services.interfaces.interface_genre_service import IGenreService

from fastapi import Depends

from .base import BaseService

logger = logging.getLogger(__name__)


class GenreService(BaseService, IGenreService):
    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        cache_key = f'genre:{genre_id}'
        cached_genre = await self.cache_service.get(cache_key)

        if cached_genre:
            genre = Genre(**json.loads(cached_genre))
            return genre

        genre = await self._get_genre_from_elastic(genre_id)

        if not genre:
            return

        await self.cache_service.setex(
            cache_key,
            GENRE_CACHE_EXPIRE_IN_SECONDS,
            json.dumps(genre.to_dict(), cls=CustomJSONEncoder),
        )

        return genre

    async def get_genres(self) -> list[Genre]:
        cache_key = f'genre:list'
        cached_films = await self.cache_service.get(cache_key)
        if cached_films:
            return [Genre(**genre) for genre in json.loads(cached_films)]

        search_body = {'query': {'match_all': {}}}
        try:
            response = await self.fts_service.search(index='genres', body=search_body, size=SIZE_RESPONSE)
        except NotFoundError as e:
            logger.error(f'Error retrieving films from Elasticsearch: {e}')
            return []
        genres = [Genre(**doc['_source']) for doc in response['hits']['hits']]

        await self.cache_service.setex(
            cache_key,
            GENRE_CACHE_EXPIRE_IN_SECONDS,
            json.dumps([genre.to_dict() for genre in genres], cls=CustomJSONEncoder),
        )

        return genres

    async def _get_genre_from_elastic(self, genre_id: UUID) -> Genre:
        try:
            doc = await self.fts_service.get(index='genres', id=str(genre_id))
            return Genre(**doc['_source'])
        except NotFoundError as e:
            logger.info(f'Error retrieving genre name from Elasticsearch: {e}')


@lru_cache()
def get_genre_service(
    cache_service: ICacheService = Depends(get_cache_service),
    fts_service: IFullTextSearchService = Depends(get_full_text_search),
) -> IGenreService:
    return GenreService(cache_service, fts_service)
