import random
from functools import lru_cache
from typing import Any
from uuid import UUID

import aiohttp
from aiohttp.client_exceptions import ClientError

from core.config import settings
from core.logger import get_logger
from db.redis import get_cache
from services.announcement.repositories import _protocols
from services.booking import layer_models
from utils.auth import _headers

logger = get_logger(__name__)


class RatingMockRepository(_protocols.RatingRepositoryProtocol):
    def __init__(self) -> None:
        self.redis = get_cache()
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


class RatingAPIReRepository(_protocols.RatingRepositoryProtocol):
    def __init__(self) -> None:
        self.redis = get_cache()
        self.rating_endpoint = settings.rating.uri  # TODO
        self._headers = _headers()
        logger.info('RatingMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, user_id: str | UUID) -> layer_models.RatingToResponse:
        if _cache := await self._get_from_cache(f'rating:{user_id}'):
            logger.info('RatingToResponse from cache')
            return layer_models.RatingToResponse(**_cache)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.rating_endpoint}{user_id}',
                    headers=self._headers,
                ) as resp:
                    _rating = await resp.json()
                    logger.debug(f'Get rating <{user_id}>: <{_rating}>')
                    # if settings.debug.DEBUG:  # noqa: E800
                    #     _duration = 0  # noqa: E800

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None
        # data = layer_models.MovieToResponse(  # noqa: E800
        #     movie_id=str(movie_id),  # noqa: E800
        #     movie_title=_movie.get('title'),  # noqa: E800
        #     duration=_duration,  # noqa: E800
        # )  # noqa: E800
        # await self._set_to_cache(f'rating:{user_id}', data.dict())  # noqa: E800
        # logger.info('RatingToResponse set to cache')  # noqa: E800
        # return data  # noqa: E800


@lru_cache()
def get_rating_repo() -> _protocols.RatingRepositoryProtocol:
    return RatingMockRepository()
