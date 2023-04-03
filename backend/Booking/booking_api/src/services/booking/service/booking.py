from enum import Enum
from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

import utils.exceptions as exc
from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.booking import layer_models, layer_payload
from services.booking.repositories.booking_repo import BookingSqlachemyRepository, get_booking_repo

logger = get_logger(__name__)


class Permission(int, Enum):
    super = 0
    author = 1
    guest = 2


class BookingService:
    def __init__(self, repo: BookingSqlachemyRepository, cache: RedisCache) -> None:
        self.repo = repo
        self.redis = cache
        logger.info('ABookingServic init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _check_permissions(self, user: dict, booking_id: str | UUID) -> Permission:
        try:
            _data: layer_models.PGBooking = await self.repo._get(booking_id)
        except exc.NotFoundError:
            raise

        if str(user.get('user_id')) == str(_data.author_id):
            return Permission.author
        elif str(user.get('user_id')) == str(_data.guest_id):
            return Permission.guest
        elif user.get('claims').get('is_super'):
            return Permission.super
        logger.info(f'Permission denied <{user.get("user_id")}>')
        raise exc.NoAccessError

    async def get_one(self, booking_id: str | UUID, user: dict) -> layer_models.DetailBookingResponse:
        try:
            prem: Permission = await self._check_permissions(user, booking_id)
            if prem.value in [0, 1, 2]:
                return await self.repo.get_by_id(booking_id)
        except (exc.NotFoundError, exc.NoAccessError):
            raise

    async def create(
        self,
        announce_id: str | UUID,
        user: dict,
    ) -> layer_models.DetailBookingResponse:
        try:
            _id = await self.repo.create(announce_id=announce_id, user_id=user.get('user_id'))
            logger.info(f'[+] Create booking <{_id}>')
        except exc.UniqueConstraintError:
            raise
        return await self.repo.get_by_id(_id)

    async def update(
        self,
        user: dict,
        booking_id: str | UUID,
        new_status: layer_payload.APIUpdatePayload,
    ) -> layer_models.DetailBookingResponse:
        try:
            prem: Permission = await self._check_permissions(user, booking_id)
            if prem.value in [1, 2]:
                await self.repo.update(
                    user_id=user.get('user_id'),
                    booking_id=booking_id,
                    new_status=new_status,
                )
        except (exc.NoAccessError, exc.NotFoundError):
            raise
        return await self.repo.get_by_id(booking_id)

    async def delete(
        self,
        user: dict,
        booking_id: str | UUID,
    ) -> None:
        try:
            prem: Permission = await self._check_permissions(user, booking_id)
            if prem.value in [0, 1]:
                await self.repo.delete(booking_id=booking_id)
        except (exc.NoAccessError, exc.NotFoundError):
            raise

    async def get_multy(
        self,
        user: dict,
        query: layer_payload.APIMultyPayload,
    ) -> list[layer_models.BookingResponse]:
        try:
            return await self.repo.get_multy(query=query, user_id=user.get('user_id'))
        except exc.ValueMissingError:
            raise

    async def sudo_get_multy(
        self,
        user: dict,
        query: layer_payload.SudoAPIMultyPayload,
    ) -> list[layer_models.BookingResponse]:
        return await self.repo.sudo_get_multy(query=query, user_id=user.get('user_id'))


@lru_cache()
def get_booking_service(
    repo: BookingSqlachemyRepository = Depends(get_booking_repo),
    cache: CacheProtocol = Depends(get_cache),
) -> BookingService:
    return BookingService(repo, cache)
