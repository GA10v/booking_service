from enum import Enum
from functools import lru_cache
from typing import Any
from uuid import UUID

from fastapi import Depends

import utils.exceptions as exc
from core.config import settings
from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.booking import layer_models, layer_payload
from services.booking.repositories import _protocols, announce_repo, booking_repo, movie_repo, rating_repo, user_repo

logger = get_logger(__name__)


class Permission(int, Enum):
    super = 0
    author = 1
    guest = 2


class BookingService:
    def __init__(
        self,
        repo: _protocols.BookingRepositoryProtocol,
        user_repo: _protocols.UserRepositoryProtocol,
        movie_repo: _protocols.MovieRepositoryProtocol,
        rating_repo: _protocols.RatingRepositoryProtocol,
        announce_repo: _protocols.AnnouncementRepositoryProtocol,
        cache: RedisCache,
    ) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.movie_repo = movie_repo
        self.rating_repo = rating_repo
        self.announce_repo = announce_repo
        self.redis = cache
        logger.info('BookingServic init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _check_permissions(self, user: dict, booking_id: str | UUID) -> Permission:
        try:
            _data: layer_models.PGBooking = await self.repo.get_by_id(booking_id)
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
        """Получение полной информации о заявке.

        :param booking_id: id заявки
        :param user: информация о пользователе
        :return: layer_models.PGBooking
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises NoAccessError: Если у пользователя нет прав
        """
        try:
            prem: Permission = await self._check_permissions(user, booking_id)
            if prem.value in [0, 1, 2]:
                _booking: layer_models.PGBooking = await self.repo.get_by_id(booking_id)
        except (exc.NotFoundError, exc.NoAccessError):
            raise

        _author = await self.user_repo.get_by_id(_booking.author_id)
        logger.info(f'Get user <{_booking.author_id}>: <{_author}>')

        _guest = await self.user_repo.get_by_id(_booking.guest_id)
        logger.info(f'Get user <{_booking.guest_id}>: <{_guest}>')

        _announce = await self.announce_repo.get_by_id(_booking.announcement_id)
        logger.info(f'Get announce <{_booking.announcement_id}>: <{_announce}>')

        _movie = await self.movie_repo.get_by_id(_announce.movie_id)
        logger.info(f'Get movie <{_announce.movie_id}>: <{_movie}>')

        _author_rating = await self.rating_repo.get_by_id(_booking.author_id)
        logger.info(f'Get rating <{_booking.author_id}>: <{_author_rating}>')

        _guest_rating = await self.rating_repo.get_by_id(_booking.guest_id)
        logger.info(f'Get rating <{_booking.guest_id}>: <{_guest_rating}>')

        return layer_models.DetailBookingResponse(
            id=_booking.id,
            announcement_id=_booking.announcement_id,
            movie_title=_movie.movie_title,
            author_name=_author.user_name,
            guest_name=_guest.user_name,
            author_status=_booking.author_status,
            guest_status=_booking.guest_status,
            author_rating=_author_rating.user_raring,
            event_time=_booking.event_time,
            guest_rating=_guest_rating.user_raring,
        )

    async def create(
        self,
        announce_id: str | UUID,
        user: dict,
    ) -> layer_models.DetailBookingResponse:
        """Создание новой заявки.

        :param announce_id: id объявления
        :param user: информация о пользователе
        :return подробная информация о заявке
        :raises UniqueConstraintError: если запист уже существует в базе
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises NoAccessError: если объявление не в статусе Alive
        """
        try:
            _announce: layer_models.AnnounceToResponse = await self.announce_repo.get_by_id(announce_id)
            logger.info(f'Get announcement <{announce_id}>: <{_announce}>')
        except exc.NotFoundError:
            raise

        if not settings.debug.DEBUG:  # noqa: SIM102
            # Объявление должно быть в статусе Alive
            if _announce.status != layer_models.EventStatus.Alive.value:
                raise exc.NoAccessError
        # Автор объявления не может быть гостем
        if str(_announce.author_id) == str(user.get('user_id')):
            raise exc.NoAccessError

        try:
            _id = await self.repo.create(announce=_announce, user_id=user.get('user_id'))
            logger.info(f'[+] Create booking <{_id}>')
        except exc.UniqueConstraintError:
            raise
        return await self.get_one(_id, user=user)

    async def update(
        self,
        user: dict,
        booking_id: str | UUID,
        new_status: layer_payload.APIUpdatePayload,
    ) -> layer_models.DetailBookingResponse:
        """
        Изменить свой статус в заявке.

        :param user: информация о пользователе
        :param booking_id: id заявки
        :param new_status: новый статус
        :return подробная информация о заявке
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises UniqueConstraintError: если запист уже существует в базе
        :raises NoAccessError: если у пользователя нет прав на изменение заявки
        """

        # TODO: переводить статус в Closed, когда все места заняты

        if not settings.debug.DEBUG:  # noqa: SIM102
            # проверяем, что объявление живое
            try:
                _booking: layer_models.PGBooking = await self.repo.get_by_id(booking_id)

                _announce: layer_models.AnnounceToResponse = await self.announce_repo.get_by_id(
                    _booking.announcement_id,
                )
                logger.info(f'Get announce <{_booking.announcement_id}>: <{_announce}>')

                if _announce.status.value not in [
                    layer_models.EventStatus.Alive.value,
                    layer_models.EventStatus.Closed.value,
                ]:
                    raise exc.NoAccessError
            except (exc.NoAccessError, exc.NotFoundError):
                raise

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
        return

    async def delete(
        self,
        user: dict,
        booking_id: str | UUID,
    ) -> None:
        """
        Удаление заявки.

        :param user: информация о пользователе
        :param announce_id: id заявки
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises NoAccessError: если у пользователя нет прав на изменение заявки
        """

        # TODO: переводить статус в Alive, когда освободилось место

        try:
            prem: Permission = await self._check_permissions(user, booking_id)
            if prem.value in [0, 1, 2]:
                await self.repo.delete(booking_id=booking_id)
        except (exc.NoAccessError, exc.NotFoundError):
            raise

    async def get_multy(
        self,
        user: dict,
        query: layer_payload.APIMultyPayload,
    ) -> list[layer_models.BookingResponse]:
        """Получение заявок по условию.

        :param user: информация о пользователе
        :param query: данные для фильтрации запроса к БД
        :return: список заявок
        """
        try:
            return await self.repo.get_multy(query=query, user_id=user.get('user_id'))
        except exc.ValueMissingError:
            raise

    async def sudo_get_multy(
        self,
        user: dict,
        query: layer_payload.SudoAPIMultyPayload,
    ) -> list[layer_models.BookingResponse]:
        return await self.repo.sudo_get_multy(query=query)


@lru_cache()
def get_booking_service(
    repo: _protocols.BookingRepositoryProtocol = Depends(booking_repo.get_booking_repo),
    user_repo: _protocols.UserRepositoryProtocol = Depends(user_repo.get_user_repo),
    movie_repo: _protocols.MovieRepositoryProtocol = Depends(movie_repo.get_movie_repo),
    rating_repo: _protocols.RatingRepositoryProtocol = Depends(rating_repo.get_rating_repo),
    announce_repo: _protocols.AnnouncementRepositoryProtocol = Depends(announce_repo.get_announcement_repo),
    cache: CacheProtocol = Depends(get_cache),
) -> BookingService:
    return BookingService(repo, user_repo, movie_repo, rating_repo, announce_repo, cache)
