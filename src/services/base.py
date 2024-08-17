from elasticsearch import AsyncElasticsearch
from redis import Redis


class BaseService:
    def __init__(self, cache_service: Redis, fts_service: AsyncElasticsearch):
        self.cache_service = cache_service
        self.fts_service = fts_service
