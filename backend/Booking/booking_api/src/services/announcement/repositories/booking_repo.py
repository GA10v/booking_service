from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.announcement import layer_models
from services.announcement.repositories import _protocols, rating_repo, user_repo

logger = get_logger(__name__)


class BookingMockRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self, cache: RedisCache) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.redis = cache
        logger.info('BookingMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _fake_boking(self) -> layer_models.BookingToDetailResponse:
        return layer_models.BookingToDetailResponse(
            guest_name=await self.user_repo.get_by_id('fake_uuid'),
            guest_rating=await self.rating_repo.get_by_id('fake_uuid'),
            guest_status=True,
            author_status=True,
        )

    async def get_by_id(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        return [await self._fake_boking() for _ in range(5)]


class BookingSqlachemyRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self, cache: RedisCache) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.redis = cache
        logger.info('BookingSqlachemyRepository init ...')
        ...

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)


@lru_cache()
def get_booking_repo(cache: CacheProtocol = Depends(get_cache)) -> _protocols.BookingRepositoryProtocol:
    return BookingMockRepository(cache)
