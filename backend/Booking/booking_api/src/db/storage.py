from abc import ABC, abstractmethod
from typing import Any, Union

from databases import Database
from sqlalchemy.sql import Delete, Insert, Select, Update

from core.config import settings


class StorageProtocol(ABC):
    @abstractmethod
    async def execute(self, query: Union[Insert, Update, Delete], values: Any) -> None:
        ...

    @abstractmethod
    async def get_one(self, query: Select) -> dict:
        ...

    @abstractmethod
    async def get_multy(self, query: Select) -> list[dict]:
        ...


class PGStorage(StorageProtocol):
    def __init__(self) -> None:
        self.session = Database(url=settings.postgres.uri)

    async def __aenter__(self) -> 'PGStorage':
        await self.session.connect()
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.disconnect()

    async def execute(self, query: Union[Insert, Update, Delete], values: Any) -> None:
        return await self.session.execute(query, values)

    async def get_one(self, query: Select) -> dict:
        return await self.session.fetch_one(query)

    async def get_multy(self, query: Select) -> list[dict]:
        return await self.session.fetch_all(query)
