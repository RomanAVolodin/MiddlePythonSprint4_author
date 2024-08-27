import json
import logging
from functools import lru_cache

from core.config import PERSON_CACHE_EXPIRE_IN_SECONDS
from db.cache_service import ICacheService, get_cache_service
from db.full_text_search_service import IFullTextSearchService, get_full_text_search
from elasticsearch import NotFoundError
from models.film import CustomJSONEncoder
from models.persons import FilmRoles, Person, PersonFilm
from pydantic import UUID4
from services.interfaces.interface_person_service import IPersonService

from fastapi import Depends

from .base import BaseService

logger = logging.getLogger(__name__)


class PersonService(BaseService, IPersonService):
    async def get_by_id(self, person_id: UUID4) -> Person | None:
        cache_key = f'person:{person_id}'
        cached_person = await self.cache_service.get(cache_key)
        if cached_person:
            person = Person(**json.loads(cached_person))
            return person

        try:
            person_res = await self.fts_service.get(index='persons', id=person_id)
        except NotFoundError as e:
            logger.info(f'Error retrieving person from Elasticsearch: {e}')
            return None
        person_data = person_res['_source']

        films_search_results = await self.get_film_search_by_person_id(person_id)
        person_films = await self.get_person_films(person_id, films_search_results)

        person = Person(
            **{
                'uuid': person_data['id'],
                'full_name': person_data['full_name'],
                'films': person_films,
            }
        )
        await self.cache_service.setex(
            cache_key,
            PERSON_CACHE_EXPIRE_IN_SECONDS,
            json.dumps(person.to_dict(), cls=CustomJSONEncoder),
        )

        return person

    async def get_person_films(self, person_id: UUID4, films_search_results) -> list[FilmRoles]:
        person_films = []
        for film_hit in films_search_results['hits']['hits']:
            film_data = film_hit['_source']
            roles = []

            roles.extend(['actor' for actor in film_data.get('actors', []) if actor.get('id') == str(person_id)])
            roles.extend(
                ['director' for director in film_data.get('directors', []) if director.get('id') == str(person_id)]
            )
            roles.extend(['writer' for writer in film_data.get('writers', []) if writer.get('id') == str(person_id)])

            person_films.append(FilmRoles(uuid=film_data['id'], roles=roles))
        return person_films

    async def get_films_by_person_id(self, person_id: UUID4) -> list[PersonFilm]:
        cache_key = f'person_film:{person_id}'
        cached_person_film = await self.cache_service.get(cache_key)
        if cached_person_film:
            films = [PersonFilm(**film) for film in json.loads(cached_person_film)]
            return films

        films_search_results = await self.get_film_search_by_person_id(person_id)
        films = [PersonFilm(**doc['_source']) for doc in films_search_results['hits']['hits']]

        await self.cache_service.setex(
            cache_key,
            PERSON_CACHE_EXPIRE_IN_SECONDS,
            json.dumps([film.to_dict() for film in films], cls=CustomJSONEncoder),
        )

        return films

    async def get_film_search_by_person_id(self, person_id):
        search_body = {
            'query': {
                'bool': {
                    'should': [
                        {
                            'nested': {
                                'path': 'actors',
                                'query': {'match': {'actors.id': str(person_id)}},
                            }
                        },
                        {
                            'nested': {
                                'path': 'directors',
                                'query': {'match': {'directors.id': str(person_id)}},
                            }
                        },
                        {
                            'nested': {
                                'path': 'writers',
                                'query': {'match': {'writers.id': str(person_id)}},
                            }
                        },
                    ]
                }
            }
        }
        elastic_film_search_by_person_id = await self.fts_service.search(index='movies', body=search_body)
        return elastic_film_search_by_person_id

    async def get_persons(self, page_size: int, page_number: int, query: str | None) -> list[Person]:
        cache_key = f'persons:{page_number}:{page_size}:{query}'
        cached_persons = await self.cache_service.get(cache_key)
        if cached_persons:
            return [Person(**person) for person in json.loads(cached_persons)]
        search_body = {
            'size': page_size,
            'from': (page_number - 1) * page_size,
            'query': {'bool': {'must': []}},
        }
        if query:
            search_body['query']['bool']['must'].append(
                {
                    'match': {
                        'full_name': query,
                    }
                }
            )
        search_results = await self.fts_service.search(index='persons', body=search_body)

        persons = []
        for hit in search_results['hits']['hits']:
            person_id = hit['_source']['id']

            films_search_results = await self.get_film_search_by_person_id(person_id)

            person_films = await self.get_person_films(person_id, films_search_results)

            persons.append(
                Person(
                    uuid=person_id,
                    full_name=hit['_source']['full_name'],
                    films=person_films,
                )
            )

        await self.cache_service.setex(
            cache_key,
            PERSON_CACHE_EXPIRE_IN_SECONDS,
            json.dumps([person.to_dict() for person in persons], cls=CustomJSONEncoder),
        )

        return persons


@lru_cache()
def get_persons_service(
    cache_service: ICacheService = Depends(get_cache_service),
    fts_service: IFullTextSearchService = Depends(get_full_text_search),
) -> IPersonService:
    return PersonService(cache_service, fts_service)
