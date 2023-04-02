from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

import utils.exceptions as exc
from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.announcement import layer_models, layer_payload
from services.announcement.repositories.announce_repo import AnnounceSqlachemyRepository, get_announcement_repo

logger = get_logger(__name__)


class AnnouncementService:
    def __init__(self, repo: AnnounceSqlachemyRepository, cache: RedisCache):
        self.repo = repo
        self.redis = cache
        logger.info('AnnouncementService init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _check_permissions(
        self,
        announce_id: str | UUID,
        user: dict,
    ) -> bool:
        try:
            _data = await self.repo._get(announce_id)
        except exc.NotFoundError:
            raise
        if user.get('claims').get('is_super'):
            logger.info(f'Sudo make changes <{announce_id}>')
            return True
        elif str(user.get('user_id')) == str(_data.get('author_id')):
            logger.info(f'Author make changes <{announce_id}>')
            return True

        logger.info(f'Permission denied <{user.get("user_id")}>')
        raise exc.NoAccessError

    async def get_one(self, announce_id: str | UUID) -> layer_models.DetailAnnouncementResponse:
        try:
            return await self.repo.get_by_id(announce_id)
        except exc.NotFoundError:
            raise

    async def create(
        self,
        author_id: str | UUID,
        movie_id: str | UUID,
        new_announce: layer_payload.APICreatePayload,
    ) -> layer_models.DetailAnnouncementResponse:
        try:
            _id = await self.repo.create(new_announce=new_announce, movie_id=movie_id, author_id=author_id)
            logger.info(f'[+] Create announcement <{_id}>')
        except exc.UniqueConstraintError:
            raise
        return await self.repo.get_by_id(_id)

    async def update(
        self,
        user: dict,
        announce_id: str | UUID,
        payload: layer_payload.APIUpdatePayload,
    ) -> layer_models.DetailAnnouncementResponse:
        if await self._check_permissions(announce_id=announce_id, user=user):
            try:
                await self.repo.update(announce_id=announce_id, update_announce=payload)
            except exc.UniqueConstraintError:
                raise
            return await self.repo.get_by_id(announce_id)

    async def delete(
        self,
        announce_id: str | UUID,
        user: dict,
    ) -> None:
        if await self._check_permissions(announce_id=announce_id, user=user):
            await self.repo.delete(announce_id=announce_id)

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.AnnouncementResponse]:
        return await self.repo.get_multy(query=query, user_id=user_id)


@lru_cache()
def get_announcement_service(
    repo: AnnounceSqlachemyRepository = Depends(get_announcement_repo),
    cache: CacheProtocol = Depends(get_cache),
) -> AnnouncementService:
    return AnnouncementService(repo, cache)
