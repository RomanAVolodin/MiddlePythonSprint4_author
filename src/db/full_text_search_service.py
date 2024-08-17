from elasticsearch import AsyncElasticsearch

fts_service: AsyncElasticsearch | None = None


async def get_full_text_search() -> AsyncElasticsearch:
    return fts_service
