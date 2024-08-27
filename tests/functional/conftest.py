import asyncio

import aiohttp
import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from redis.asyncio import Redis

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def session_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(session_client: ClientSession):
    async def inner(url: str, params: dict | None = None):
        if not params:
            params = {}
        async with session_client.get(url, params=params) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return body, headers, status

    return inner


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.elastic_settings.get_host(), verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='cache_service_client', scope='session')
async def cache_service_client():
    cache_service_client = Redis(
        host=test_settings.redis_settings.host,
        port=test_settings.redis_settings.port,
    )
    yield cache_service_client
    await cache_service_client.aclose()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(index: str, index_settings: dict, data: list[dict]):
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(
            index=index, settings=index_settings.get('settings'), mappings=index_settings.get('mappings')
        )
        updated, errors = await async_bulk(client=es_client, actions=data, refresh='wait_for')

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner
