from functools import lru_cache
from typing import Any
from uuid import UUID

import aiohttp
from aiohttp.client_exceptions import ClientError
from fastapi import Depends

from core.config import settings
from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.announcement import layer_models
from services.announcement.repositories import _protocols
from utils.auth import _headers

logger = get_logger(__name__)


class MovieMockRepository(_protocols.MovieRepositoryProtocol):
    def __init__(self, cache: RedisCache) -> None:
        self.movie_endpoint = f'{settings.movie_api.uri}movie/'
        self._headers = _headers()
        self.redis = cache

        logger.info('MovieMockRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, movie_id: str | UUID) -> layer_models.MovieToResponse:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.movie_endpoint}{movie_id}',
                    headers=self._headers,
                ) as resp:
                    _movie = await resp.json()
                    logger.debug(f'Get movie <{movie_id}>: <{_movie}>')

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return layer_models.MovieToResponse(
            movie_title=_movie.get('title'),
            duration=_movie.get('duration'),
        )


@lru_cache()
def get_movie_repo(cache: CacheProtocol = Depends(get_cache)) -> _protocols.MovieRepositoryProtocol:
    return MovieMockRepository(cache)
