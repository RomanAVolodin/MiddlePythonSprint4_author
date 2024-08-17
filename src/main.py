import logging
from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films, genre, persons
from core import config
from core.logger import LOGGING
from db import cache_service, full_text_search_service

log_config = (LOGGING,)
log_level = (logging.DEBUG,)


@asynccontextmanager
async def lifespan(_: FastAPI):
    cache_service.cache_service = Redis(
        host=config.settings.redis_settings.host,
        port=config.settings.redis_settings.port,
    )
    full_text_search_service.fts_service = AsyncElasticsearch(hosts=[config.settings.elastic_settings.get_host()])
    yield
    await cache_service.cache_service.close()
    await full_text_search_service.fts_service.close()


app = FastAPI(
    title=config.settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genre.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
