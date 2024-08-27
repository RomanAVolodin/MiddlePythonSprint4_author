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
from tests.functional.testdata import persons


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_edge_cases)
@pytest.mark.asyncio
async def test_find_person_edge_cases(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    await _setup_test_environment(es_write_data, person_uuids=[person_id])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}')

    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        assert body.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_edge_cases)
@pytest.mark.asyncio
async def test_find_person_film_edge_cases(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    await _setup_test_environment(es_write_data, person_uuids=[person_id])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}/film')
    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        for film in body:
            assert film.keys() == expected_answer.get('film_fields')


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_valid_data)
@pytest.mark.asyncio
async def test_find_person_valid(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    await _setup_test_environment(es_write_data, person_uuids=[person_id])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}')

    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        assert body.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_valid_data)
@pytest.mark.asyncio
async def test_find_person_film_valid(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    await _setup_test_environment(es_write_data, person_uuids=[person_id])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}/film')

    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        for film in body:
            assert film.keys() == expected_answer.get('film_fields')


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_invalid_data)
@pytest.mark.asyncio
async def test_find_person_invalid(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    await _setup_test_environment(es_write_data, person_uuids=[uuid.uuid4()])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}')

    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_invalid_data)
@pytest.mark.asyncio
async def test_find_person_film_invalid(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    await _setup_test_environment(es_write_data, person_uuids=[uuid.uuid4()])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}/film')

    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')


@pytest.mark.parametrize('query_data, expected_answer', persons.find_persons_films)
@pytest.mark.asyncio
async def test_find_person_films(es_write_data, make_get_request, query_data, expected_answer):
    person_id = query_data.get('person_id')
    films_amount = query_data.get('films_amount')
    await _setup_test_environment(
        es_write_data, person_uuids=[person_id for _ in range(films_amount)], films_amount=films_amount
    )

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}/film')

    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('films_amount')
    if expected_answer.get('status') == HTTPStatus.OK:
        for film in body:
            assert film.keys() == expected_answer.get('film_fields')


@pytest.mark.parametrize('query_data, expected_answer', persons.person_redis_data)
@pytest.mark.asyncio
async def test_get_person_redis(es_write_data, make_get_request, cache_service_client, query_data, expected_answer):
    person_id = query_data.get('person_id')
    cache_key = f'person:{person_id}'
    await cache_service_client.delete(cache_key)
    cached_person = await cache_service_client.get(cache_key)

    assert cached_person is None

    await _setup_test_environment(es_write_data, person_uuids=[person_id])

    url = urljoin(test_settings.service_url, f'/api/v1/persons/{person_id}')

    body, headers, status = await make_get_request(url, query_data)

    cached_person_raw = await cache_service_client.get(cache_key)
    cached_person = json.loads(cached_person_raw)

    assert cached_person.get('uuid') == person_id
    assert status == expected_answer.get('status')
    if expected_answer.get('status') == HTTPStatus.OK:
        assert body.keys() == expected_answer.get('fields')


async def _generate_persons(
    persons_amount: int = 1, person_uuids: list[uuid.UUID] | None = None, person_names: list[str] | None = None
) -> list[dict]:
    es_data = [
        {
            'id': str(uuid.uuid4()) if not person_uuids else person_uuids[idx],
            'full_name': 'John Johnson' if not person_names else person_names[idx],
            'last_change_date': datetime.datetime.now().isoformat(),
        }
        for idx in range(persons_amount)
    ]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'persons', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


async def _setup_test_environment(
    es_write_data, persons_amount: int = 1, person_uuids: list[uuid.UUID] | None = None, films_amount: int = 1
):
    elastic_conf = test_settings.elastic_settings
    bulk_query: list[dict] = await _generate_persons(persons_amount, person_uuids)
    with open(elastic_conf.persons_index_filename, 'r', encoding='utf-8') as index_file:
        index_settings = json.load(index_file)
    await es_write_data(elastic_conf.persons_index, index_settings, bulk_query)
    bulk_query: list[dict] = await _generate_films(films_amount=films_amount, person_uuids=person_uuids)
    with open(elastic_conf.movies_index_filename, 'r', encoding='utf-8') as index_file:
        index_settings = json.load(index_file)
    await es_write_data(elastic_conf.movies_index, index_settings, bulk_query)


async def _generate_films(
    films_amount: int = 1, film_uuids: list[uuid.UUID] | None = None, person_uuids: list[uuid.UUID] | None = None
) -> list[dict]:
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
                {'id': str(uuid.uuid4()) if not person_uuids else person_uuids[idx], 'name': 'Ann'},
            ],
            'writers': [
                {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
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
