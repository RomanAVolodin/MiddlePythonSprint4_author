from db.interfaces.interface_cache_service import ICacheService

cache_service: ICacheService | None = None


async def get_cache_service() -> ICacheService:
    return cache_service
