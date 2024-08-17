import json
import logging
from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis import Redis

from core.config import GENRE_CACHE_EXPIRE_IN_SECONDS, SIZE_RESPONSE
from db.cache_service import get_cache_service
from db.full_text_search_service import get_full_text_search
from models.film import CustomJSONEncoder, Genre

from .base import BaseService

logger = logging.getLogger(__name__)


class GenreService(BaseService):
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
        cache_key = 'genre:list'
        cached_films = await self.cache_service.get(cache_key)
        if cached_films:
            return [Genre(**genre) for genre in json.loads(cached_films)]

        search_body = {'query': {'match_all': {}}}
        try:
            response = await self.fts_service.search(index='genres', body=search_body, size=SIZE_RESPONSE)
        except NotFoundError as e:
            logger.error('Error retrieving films from Elasticsearch: %s', e)
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
            logger.info('Error retrieving genre name from Elasticsearch: %s', e)


@lru_cache()
def get_genre_service(
    cache_service: Redis = Depends(get_cache_service),
    fts_service: AsyncElasticsearch = Depends(get_full_text_search),
) -> GenreService:
    return GenreService(cache_service, fts_service)
