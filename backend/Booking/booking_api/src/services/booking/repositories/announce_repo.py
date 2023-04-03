from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

import utils.exceptions as exc
from core.logger import get_logger
from db.models.announcement import Announcement
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, RedisCache, get_cache
from services.booking import layer_models
from services.booking.repositories import _protocols

logger = get_logger(__name__)


class AnnounceSqlachemyRepository(_protocols.AnnouncementRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: RedisCache) -> None:
        self.db = db_session
        self.redis = cache
        logger.info('AnnounceSqlachemyRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def get_by_id(self, announce_id: str | UUID) -> layer_models.AnnounceToResponse:
        _data = await self.db.get(Announcement, announce_id)
        if _data is None:
            logger.info(f'[-] Not found <{announce_id}>')
            raise exc.NotFoundError
        _data = _data._asdict()

        return layer_models.AnnounceToResponse(
            author_id=_data.get('author_id'),
            event_time=_data.get('event_time'),
            movie_id=_data.get('movie_id'),
        )


@lru_cache()
def get_announcement_repo(
    db_session: AsyncSession = Depends(get_session),
    cache: CacheProtocol = Depends(get_cache),
) -> _protocols.AnnouncementRepositoryProtocol:
    return AnnounceSqlachemyRepository(db_session, cache)
