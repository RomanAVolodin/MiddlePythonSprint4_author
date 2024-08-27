import datetime
import json
import uuid
from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from tests.functional.conftest import (
    cache_service_client,
    es_write_data,
    make_get_request,
)
from tests.functional.settings import test_settings
from tests.functional.testdata import films


@pytest.mark.parametrize('query_data, expected_answer', films.film_edge_cases_data)
@pytest.mark.asyncio
async def test_film_edge_cases(es_write_data, make_get_request, query_data, expected_answer):
    await _setup_test_environment(es_write_data, query_data.get('films_amount'))

    url = urljoin(test_settings.service_url, '/api/v1/films')
    query_data = {'page_size': query_data.get('page_size'), 'page_number': query_data.get('page_number')}
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')
    if expected_answer.get('status') == HTTPStatus.OK:
        for film in body:
            assert film.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', films.validation_genre_data)
@pytest.mark.asyncio
async def test_film_validation_genre(es_write_data, make_get_request, query_data, expected_answer):
    await _setup_test_environment(es_write_data)

    url = urljoin(test_settings.service_url, '/api/v1/films')
    query_data = {
        'genre': query_data.get('genre'),
    }
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer.get('status')


@pytest.mark.parametrize('query_data, expected_answer', films.validation_query_data)
@pytest.mark.asyncio
async def test_film_validation_query(es_write_data, make_get_request, query_data, expected_answer):
    await _setup_test_environment(es_write_data)

    url = urljoin(test_settings.service_url, '/api/v1/films')
    query_data = {
        'query': query_data.get('query'),
    }
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer.get('status')


@pytest.mark.parametrize('query_data, expected_answer', films.validation_sort_data)
@pytest.mark.asyncio
async def test_film_validation_sort(es_write_data, make_get_request, query_data, expected_answer):
    await _setup_test_environment(es_write_data)

    url = urljoin(test_settings.service_url, '/api/v1/films')
    query_data = {
        'sort': query_data.get('sort'),
    }
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        for film in body:
            assert film.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', films.validation_pages_data)
@pytest.mark.asyncio
async def test_film_validation_pages(es_write_data, make_get_request, query_data, expected_answer):
    await _setup_test_environment(es_write_data)

    url = urljoin(test_settings.service_url, '/api/v1/films')
    query_data = {
        'page_size': query_data.get('page_size'),
        'page_number': query_data.get('page_number'),
    }
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        for film in body:
            assert film.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', films.get_film_data)
@pytest.mark.asyncio
async def test_get_film(es_write_data, make_get_request, query_data, expected_answer):
    film_uuid = uuid.UUID(query_data.get('film_uuid'))

    await _setup_test_environment(es_write_data, film_uuids=[film_uuid])

    url = urljoin(test_settings.service_url, f'/api/v1/films/{str(film_uuid)}')
    query_data = {}
    body, headers, status = await make_get_request(url, query_data)

    assert status == expected_answer.get('status')


@pytest.mark.parametrize('query_data, expected_answer', films.get_film_data)
@pytest.mark.asyncio
async def test_get_film_redis(es_write_data, make_get_request, cache_service_client, query_data, expected_answer):
    film_uuid = uuid.UUID(query_data.get('film_uuid'))
    cache_key = f'film:{film_uuid}'
    await cache_service_client.delete(cache_key)
    cached_film = await cache_service_client.get(cache_key)

    assert cached_film is None

    await _setup_test_environment(es_write_data, film_uuids=[film_uuid])

    url = urljoin(test_settings.service_url, f'/api/v1/films/{str(film_uuid)}')
    query_data = {}
    body, headers, status = await make_get_request(url, query_data)

    cached_film_raw = await cache_service_client.get(cache_key)
    cached_film = json.loads(cached_film_raw)

    assert cached_film.get('id') == str(film_uuid)
    assert status == expected_answer.get('status')


async def _generate_films(films_amount: int = 1, film_uuids: list[uuid.UUID] | None = None) -> list[dict]:
    es_data = [
        {
            'id': str(uuid.uuid4()) if not film_uuids else film_uuids[idx],
            'imdb_rating': 8.5,
            'genres': ['Action', 'Sci-Fi'],
            'title': 'The Star',
            'description': 'New World',
            'file': 'c46bdb94-5177-441d-b7ab-d5dba85295fc',
            'directors_names': ['Stan'],
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [{'id': '02e304e3-1984-4d52-9f4a-b9c5713f54b3', 'name': 'Stan'}],
            'actors': [
                {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
                {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'},
            ],
            'writers': [
                {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
                {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'},
            ],
            'last_change_date': datetime.datetime.now().isoformat(),
        }
        for idx in range(films_amount)
    ]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'movies', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


async def _setup_test_environment(es_write_data, films_amount: int = 1, film_uuids: list[uuid.UUID] | None = None):
    elastic_conf = test_settings.elastic_settings
    bulk_query: list[dict] = await _generate_films(films_amount, film_uuids)
    with open(elastic_conf.movies_index_filename, 'r', encoding='utf-8') as index_file:
        index_settings = json.load(index_file)
    await es_write_data(elastic_conf.movies_index, index_settings, bulk_query)
