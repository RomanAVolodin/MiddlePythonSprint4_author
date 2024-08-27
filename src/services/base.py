from db.cache_service import ICacheService
from db.full_text_search_service import IFullTextSearchService


class BaseService:
    def __init__(self, cache_service: ICacheService, fts_service: IFullTextSearchService):
        self.cache_service = cache_service
        self.fts_service = fts_service
