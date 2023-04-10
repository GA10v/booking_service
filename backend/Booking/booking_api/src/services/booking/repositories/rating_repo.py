import random
from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.booking import layer_models
from services.booking.repositories import _protocols

logger = get_logger(__name__)


class RatingMockRepository(_protocols.RatingRepositoryProtocol):
    def __init__(self, cache: RedisCache) -> None:
        self.redis = cache
        logger.info('RatingMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, user_id: str | UUID) -> layer_models.RatingToResponse:
        if _cache := await self._get_from_cache(f'rating:{user_id}'):
            logger.info('RatingToResponse from cache')
            return layer_models.RatingToResponse(**_cache)
        data = layer_models.RatingToResponse(
            user_raring=round(random.uniform(0.0, 10.0), 1),
        )
        await self._set_to_cache(f'rating:{user_id}', data.dict())
        logger.info('RatingToResponse set to cache')
        return data


@lru_cache()
def get_rating_repo(cache: CacheProtocol = Depends(get_cache)) -> _protocols.RatingRepositoryProtocol:
    return RatingMockRepository(cache)
