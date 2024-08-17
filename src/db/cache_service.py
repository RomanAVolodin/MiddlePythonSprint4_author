from redis import Redis

cache_service: Redis | None = None


async def get_cache_service() -> Redis:
    return cache_service
