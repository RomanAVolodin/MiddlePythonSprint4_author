from abc import ABC, abstractmethod
from typing import Any


class ICacheService(ABC):
    @abstractmethod
    async def setex(self, key: str, seconds: int, value: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError
