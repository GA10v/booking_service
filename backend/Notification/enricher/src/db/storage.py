from abc import ABC, abstractmethod
from typing import Union

import asyncpg
from databases import Database
from sqlalchemy.sql import Delete, Insert, Select, Update

from core.config import settings


class StorageProtocol(ABC):
    @abstractmethod
    async def execute(self, query: Union[Select, Insert, Update, Delete]) -> list[dict] | None:
        ...


class PGStorage(StorageProtocol):
    def __init__(self) -> None:
        self.session = Database(url=settings.postgres.uri)

    async def __aenter__(self) -> 'PGStorage':
        await self.session.connect()
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.disconnect()

    async def execute(self, query: Union[Select, Insert, Update, Delete]) -> list[dict] | None:
        if query.is_select:
            return await self.session.fetch_all(query)
        return await self.session.execute(query)


class APGStorage(StorageProtocol):
    def __init__(self) -> None:
        self.pool = None

    async def __aenter__(self) -> 'PGStorage':
        self.pool = await asyncpg.create_pool(dsn=settings.postgres.a_uri)
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.pool.close()

    async def execute(self, query: Union[Select, Insert, Update, Delete]) -> list[dict] | None:
        async with self.pool.acquire() as connection:
            if query.is_select:
                result = await connection.fetchrow(query)
                return [dict(row) for row in result]
            await connection.execute(query)
