from db.interfaces.interface_full_test_search_service import IFullTextSearchService

fts_service: IFullTextSearchService | None = None


async def get_full_text_search() -> IFullTextSearchService:
    return fts_service
