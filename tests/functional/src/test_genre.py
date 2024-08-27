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
from tests.functional.testdata import genre_test_parameters


@pytest.mark.parametrize('query_data, expected_answer', genre_test_parameters.genre_get_genres_data)
@pytest.mark.asyncio
async def test_genre_get_genres(es_write_data, make_get_request, cache_service_client, query_data, expected_answer):
    await cache_service_client.flushall()

    await _setup_test_environment(es_write_data, query_data.get('genres_amount'))

    url = urljoin(test_settings.service_url, '/api/v1/genres')
    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')
    if expected_answer.get('status') == HTTPStatus.OK:
        for genre in body:
            assert genre.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', genre_test_parameters.genre_id_data)
@pytest.mark.asyncio
async def test_genre_get_by_id(es_write_data, make_get_request, cache_service_client, query_data, expected_answer):
    await cache_service_client.flushall()

    genre_uuid = uuid.UUID(query_data.get('genreuuid'))

    await _setup_test_environment(es_write_data, query_data.get('genres_amount'), genres_uuids=[genre_uuid])

    url = urljoin(test_settings.service_url, f'/api/v1/genres/{genre_uuid}')
    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')
    if expected_answer.get('status') == HTTPStatus.OK:
        assert body.keys() == expected_answer.get('fields')


@pytest.mark.parametrize('query_data, expected_answer', genre_test_parameters.genre_not_found_id_data)
@pytest.mark.asyncio
async def test_genre_get_by_id_not_found(make_get_request, query_data, expected_answer):

    genre_not_found_uuid = uuid.UUID(query_data.get('genreuuid'))

    url = urljoin(test_settings.service_url, f'/api/v1/genres/{genre_not_found_uuid}')
    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    assert body == expected_answer.get('message')


@pytest.mark.parametrize('query_data, expected_answer', genre_test_parameters.genre_incorrect_id_data)
@pytest.mark.asyncio
async def test_genre_get_by_incorrect_id(make_get_request, query_data, expected_answer):

    genre_incorrect_uuid = query_data.get('genreuuid')

    url = urljoin(test_settings.service_url, f'/api/v1/genres/{genre_incorrect_uuid}')
    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    assert body['detail'][0]['msg'].__contains__(expected_answer.get('message_part'))


@pytest.mark.parametrize('query_data, expected_answer', genre_test_parameters.genre_id_data)
@pytest.mark.asyncio
async def test_genre_cache(es_write_data, make_get_request, cache_service_client, query_data, expected_answer):
    await cache_service_client.flushall()

    genre_uuid = uuid.UUID(query_data.get('genreuuid'))
    cache_key = f'genre:{genre_uuid}'

    await _setup_test_environment(es_write_data, query_data.get('genres_amount'), genres_uuids=[genre_uuid])

    cached_genre = await cache_service_client.get(cache_key)

    assert cached_genre is None

    url = urljoin(test_settings.service_url, f'/api/v1/genres/{genre_uuid}')
    await make_get_request(url)

    cached_genre = await cache_service_client.get(cache_key)
    genre = json.loads(cached_genre)
    assert genre['id'] == str(genre_uuid)

    await cache_service_client.flushall()
    body, headers, status = await make_get_request(url)

    assert status == expected_answer.get('status')
    assert len(body) == expected_answer.get('length')
    if expected_answer.get('status') == HTTPStatus.OK:
        assert body.keys() == expected_answer.get('fields')


async def _generate_genres(genres_amount: int = 1, genres_uuids: list[uuid.UUID] | None = None) -> list[dict]:
    es_data = [
        {
            'id': str(uuid.uuid4()) if not genres_uuids else genres_uuids[idx],
            'name': f'Action test_{idx}',
            'description': f'Action desc test_{idx}',
            'last_change_date': datetime.datetime.now().isoformat(),
        }
        for idx in range(genres_amount)
    ]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'genres', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


async def _setup_test_environment(
    es_write_data,
    genres_amount: int = 1,
    genres_uuids: list[uuid.UUID] | None = None,
):

    elastic_conf = test_settings.elastic_settings
    bulk_query: list[dict] = await _generate_genres(genres_amount, genres_uuids)
    with open(elastic_conf.genres_index_filename, 'r', encoding='utf-8') as index_file:
        index_settings = json.load(index_file)
    await es_write_data(elastic_conf.genres_index, index_settings, bulk_query)
