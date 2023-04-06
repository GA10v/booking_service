import json
from abc import ABC, abstractmethod
from enum import Enum, unique

import aioredis

from core.config import settings


class CacheProtocol(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        ...

    @abstractmethod
    async def set(self, key: str, value: str, exp: int) -> None:
        ...


@unique
class MSGStatus(Enum):
    New = None
    InProcess = 0
    Error = 2
    Done = 3


class RedisCache(CacheProtocol):
    def __init__(self) -> None:
        self.session = aioredis.from_url(settings.redis.uri)

    async def get(self, key: str) -> str:
        value = await self.session.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: str, exp: int = settings.redis.EXPIRE_SEC) -> None:
        await self.session.set(key, json.dumps(value.value).encode('utf-8'), ex=exp)

    async def close(self) -> None:
        await self.session.close()
