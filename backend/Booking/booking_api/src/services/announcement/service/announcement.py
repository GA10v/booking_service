from datetime import datetime
from functools import lru_cache
from typing import Any
from uuid import UUID

import pytz
from fastapi import Depends

import utils.exceptions as exc
from core.config import settings
from core.logger import get_logger
from db.redis import CacheProtocol, RedisCache, get_cache
from services.announcement import layer_models, layer_payload
from services.announcement.repositories import (
    _protocols,
    announce_repo,
    booking_repo,
    movie_repo,
    rating_repo,
    user_repo,
)

logger = get_logger(__name__)
utc = pytz.UTC


class AnnouncementService:
    def __init__(
        self,
        repo: _protocols.AnnouncementRepositoryProtocol,
        user_repo: _protocols.UserRepositoryProtocol,
        movie_repo: _protocols.MovieRepositoryProtocol,
        rating_repo: _protocols.RatingRepositoryProtocol,
        booking_repo: _protocols.BookingRepositoryProtocol,
        cache: RedisCache,
    ):
        self.repo = repo
        self.user_repo = user_repo
        self.movie_repo = movie_repo
        self.rating_repo = rating_repo
        self.booking_repo = booking_repo
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
        """
        Служебный метод. Проверка прав пользователя.

        :param announce_id: id объявления
        :param user: информация о пользователе
        :return: bool флаг
        :raises NoAccessError: если пользователь не sudo, author или guest
        """
        try:
            _data: layer_models.PGAnnouncement = await self.repo.get_by_id(announce_id)
        except exc.NotFoundError:
            raise
        if user.get('claims').get('is_super'):
            logger.info(f'Sudo make changes <{announce_id}>')
            return True
        elif str(user.get('user_id')) == str(_data.author_id):
            logger.info(f'Author make changes <{announce_id}>')
            return True

        logger.info(f'Permission denied <{user.get("user_id")}>')
        raise exc.NoAccessError

    async def get_one(self, announce_id: str | UUID) -> layer_models.DetailAnnouncementResponse:
        """
        Получение полной информации Announcement.

        :param announce_id: id объявления
        :return: подробная информация о событии
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        try:
            _announce: layer_models.PGAnnouncement = await self.repo.get_by_id(announce_id)
        except exc.NotFoundError:
            raise

        # TODO: CACHE

        _user = await self.user_repo.get_by_id(_announce.author_id)
        logger.info(f'Get user <{announce_id}>: <{_user}>')

        # TODO: CACHE

        _movie = await self.movie_repo.get_by_id(_announce.movie_id)
        logger.info(f'Get movie <{_announce.movie_id}>: <{_movie}>')

        # TODO: CACHE

        _rating = await self.rating_repo.get_by_id(_announce.author_id)
        logger.info(f'Get author_rating <{_announce.author_id}>: <{_rating}>')

        _guests = await self.booking_repo.get_by_id(announce_id=announce_id)
        logger.info(f'Get guest_list <{announce_id}>: <{_guests}>')
        if not _guests:
            _guests = []

        _confirmed_list = await self.booking_repo.get_confirmed_list(announce_id=announce_id)

        _tickets_left = _announce.tickets_count - len(_confirmed_list)

        return layer_models.DetailAnnouncementResponse(
            id=_announce.id,
            created=_announce.created,
            modified=_announce.modified,
            status=_announce.status.value,
            title=_announce.title,
            description=_announce.description,
            sub_only=_announce.sub_only,
            is_free=_announce.is_free,
            tickets_count=_announce.tickets_count,
            tickets_left=_tickets_left,
            event_time=_announce.event_time,
            event_location=_announce.event_location,
            author_name=_user.user_name,
            guest_list=_guests,
            author_rating=_rating.user_raring,
            movie_title=_movie.movie_title,
            duration=_movie.duration,
        )

    async def create(
        self,
        author_id: str | UUID,
        movie_id: str | UUID,
        new_announce: layer_payload.APICreatePayload,
    ) -> layer_models.DetailAnnouncementResponse:
        """
        Создание нового объявления.

        :param author_id: id автора
        :param movie_id: id контента
        :param new_announce: данные из API для создания объявления
        :return: подробная информация о событии
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        try:

            # TODO: CACHE

            _movie = await self.movie_repo.get_by_id(movie_id)
            logger.info(f'Get movie <{movie_id}>: <{_movie}>')
            _id = await self.repo.create(new_announce=new_announce, movie=_movie, author_id=author_id)
            logger.info(f'[+] Create announcement <{_id}>')
        except exc.UniqueConstraintError:
            raise
        return await self.get_one(_id)

    async def update(
        self,
        user: dict,
        announce_id: str | UUID,
        payload: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        Изменить данные в объявлении.

        :param user: информация о пользователе
        :param announce_id: id объявления
        :param payload: данные из API для изменения объявления
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises UniqueConstraintError: если запист уже существует в базе
        :raises NoAccessError: Если у пользователя нет прав на изменение объявления
        """
        if not settings.debug.DEBUG:  # noqa: SIM102
            # Событе не может быть Alive, если event_time истек
            if (payload.event_time < utc.localize(datetime.utcnow())) and (
                payload.status.value == layer_models.EventStatus.Alive.value
            ):
                raise exc.UniqueConstraintError
        # Только Watcher может присваивать статус Done
        if payload.status.value == layer_models.EventStatus.Done.value:
            raise exc.UniqueConstraintError
        # Проверяем, что запись есть в БД
        try:
            _announce: layer_models.PGAnnouncemen = await self.repo.get_by_id(announce_id)
        except exc.NotFoundError:
            raise
        # Нельзя менять объявления в статусе Done
        if _announce.status == layer_models.EventStatus.Done.value:
            raise exc.UniqueConstraintError

        # Только автор и sudo могут вносить изменения
        if not await self._check_permissions(announce_id=announce_id, user=user):
            raise exc.NoAccessError
        try:
            await self.repo.update(announce_id=announce_id, update_announce=payload)
        except exc.UniqueConstraintError:
            raise

    async def delete(
        self,
        announce_id: str | UUID,
        user: dict,
    ) -> None:
        """
        Удаление объявления.

        :param announce_id: id объявления
        :param user: информация о пользователе
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises NoAccessError: Если у пользователя нет прав на изменение объявления
        """
        # Проверяем, что запись есть в БД
        try:
            await self.repo.get_by_id(announce_id)
        except exc.NotFoundError:
            raise
        # Только автор и sudo могут вносить изменения
        if await self._check_permissions(announce_id=announce_id, user=user):
            await self.repo.delete(announce_id=announce_id)
            return
        raise exc.NoAccessError

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.AnnouncementResponse]:
        """
        Получение списка объявлений.

        :param user_id: id пользователя
        :param query: данные для поиска
        :return: список объявлений
        """

        # TODO: CACHE

        _user: layer_models.UserToResponse = await self.user_repo.get_by_id(user_id)
        logger.info(f'Get user <{user_id}>: <{_user}>')

        return await self.repo.get_multy(query=query, user=_user)


@lru_cache()
def get_announcement_service(
    repo: _protocols.AnnouncementRepositoryProtocol = Depends(announce_repo.get_announcement_repo),
    user_repo: _protocols.UserRepositoryProtocol = Depends(user_repo.get_user_repo),
    movie_repo: _protocols.MovieRepositoryProtocol = Depends(movie_repo.get_movie_repo),
    rating_repo: _protocols.RatingRepositoryProtocol = Depends(rating_repo.get_rating_repo),
    booking_repo: _protocols.BookingRepositoryProtocol = Depends(booking_repo.get_booking_repo),
    cache: CacheProtocol = Depends(get_cache),
) -> AnnouncementService:
    return AnnouncementService(repo, user_repo, movie_repo, rating_repo, booking_repo, cache)
