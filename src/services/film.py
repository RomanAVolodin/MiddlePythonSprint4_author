import json
import logging
from functools import lru_cache
from uuid import UUID

from core.config import FILM_CACHE_EXPIRE_IN_SECONDS
from db.cache_service import ICacheService, get_cache_service
from db.full_text_search_service import IFullTextSearchService, get_full_text_search
from elasticsearch import NotFoundError
from models.film import CustomJSONEncoder, Film, Genre
from services.interfaces.interface_film_service import IFilmService

from fastapi import Depends

from .base import BaseService

logger = logging.getLogger(__name__)


class FilmService(BaseService, IFilmService):
    async def get_by_id(self, film_id: str) -> Film | None:
        cache_key = f'film:{film_id}'
        cached_film = await self.cache_service.get(cache_key)

        if cached_film:
            film = Film(**json.loads(cached_film))
            return film

        film = await self._get_film_from_elastic(film_id)
        if not film:
            return

        await self.cache_service.setex(
            cache_key,
            FILM_CACHE_EXPIRE_IN_SECONDS,
            json.dumps(film.to_dict(), cls=CustomJSONEncoder),
        )
        return film

    async def get_films(
        self,
        page_size: int,
        page_number: int,
        sort: str | None,
        genre: UUID | None,
        query: str | None,
    ) -> list[Film]:
        cache_key = f'films:{sort}:{page_number}:{page_size}:{genre}:{query}'
        cached_films = await self.cache_service.get(cache_key)

        if cached_films:
            return [Film(**film) for film in json.loads(cached_films)]

        from_item = (page_number - 1) * page_size

        search_body = {
            'size': page_size,
            'from': from_item,
            'query': {'bool': {'must': []}},
        }

        if sort:
            sort_field = sort.lstrip('-')
            sort_order = 'desc' if sort.startswith('-') else 'asc'
            search_body['sort'] = {sort_field: {'order': sort_order}}

        if genre:
            genre_name = await self.get_genre_name_from_es(genre) or 'NO_GENRE'
            if genre_name:
                search_body['query']['bool']['must'].append(
                    {
                        'match': {
                            'genres': genre_name,
                        }
                    }
                )

        if query:
            search_body['query']['bool']['must'].append(
                {
                    'match': {
                        'title': query,
                    }
                }
            )

        try:
            response = await self.fts_service.search(index='movies', body=search_body)
        except NotFoundError as e:
            logger.error(f'Error retrieving films from Elasticsearch: {e}')
            return []
        films = [Film(**doc['_source']) for doc in response['hits']['hits']]

        await self.cache_service.setex(
            cache_key,
            FILM_CACHE_EXPIRE_IN_SECONDS,
            json.dumps([film.to_dict() for film in films], cls=CustomJSONEncoder),
        )
        return films

    async def get_genre_name_from_es(self, genre_id: UUID) -> str | None:
        try:
            doc = await self.fts_service.get(index='genres', id=str(genre_id))
            return Genre(**doc['_source']).name
        except NotFoundError as e:
            logger.info(f'Error retrieving genre name from Elasticsearch: {e}')

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.fts_service.get(index='movies', id=film_id)
        except NotFoundError as e:
            logger.info(f'Error retrieving film from Elasticsearch: {e}')
            return None
        return Film(**doc['_source'])


@lru_cache()
def get_film_service(
    cache_service: ICacheService = Depends(get_cache_service),
    fts_service: IFullTextSearchService = Depends(get_full_text_search),
) -> IFilmService:
    return FilmService(cache_service, fts_service)
