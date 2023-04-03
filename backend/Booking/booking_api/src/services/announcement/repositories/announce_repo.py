from functools import lru_cache
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy.exc as sqlalch_exc
from fastapi import Depends
from sqlalchemy import insert, select, update

import utils.exceptions as exc
from core.logger import get_logger
from db.models.announcement import Announcement
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, RedisCache, get_cache
from services.announcement import layer_models, layer_payload
from services.announcement.repositories import _protocols, booking_repo, movie_repo, rating_repo, user_repo

logger = get_logger(__name__)


class AnnounceSqlachemyRepository(_protocols.AnnouncementRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: RedisCache) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.movie_repo = movie_repo.get_movie_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.booking_repo = booking_repo.get_booking_repo()
        self.db = db_session
        self.redis = cache
        logger.info('AnnounceSqlachemyRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _get(self, announce_id: str | UUID) -> dict:
        """
        Служебный метод. Возвращает запист Announcement из БД.

        :param announce_id: id объявления
        :return: dict данные из БД по id
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        data = await self.db.get(Announcement, announce_id)
        if data is None:
            logger.info(f'[-] Not found <{announce_id}>')
            raise exc.NotFoundError
        return data._asdict()

    async def get_by_id(self, announce_id: str | UUID) -> layer_models.DetailAnnouncementResponse:
        """
        Получение полной информации о Announcement.

        :param announce_id: id объявления
        :return: подробная информация о событии
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        query = select(Announcement).filter(Announcement.id == announce_id)
        _res = await self.db.execute(query)
        scalar_result = _res.scalars().all()

        if len(scalar_result) == 0:
            logger.info(f'[-] Not found <{announce_id}>')
            raise exc.NotFoundError

        _announce = scalar_result[0]._asdict()
        logger.info(f'Get _res <{announce_id}>: <{_announce}>')

        _user = await self._get_from_cache(f'user_info:{_announce.get("author_id")}')
        if not _user:
            _user = await self.user_repo.get_by_id(_announce.get('author_id'))
            await self._set_to_cache(f'user_info:{_announce.get("author_id")}', _user)
            logger.info(f'Get user <{announce_id}>: <{_user}>')

        _movie = await self.movie_repo.get_by_id(_announce.get('movie_id'))
        logger.info(f'Get movie <{_announce.get("movie_id")}>: <{_movie}>')

        _guests = await self.booking_repo.get_by_id(announce_id=announce_id)
        logger.info(f'Get guest_list <{announce_id}>: <{_guests}>')
        if not _guests:
            _guests = []

        _tickets_left = _announce.get('tickets_count') - len(_guests)

        _rating = await self._get_from_cache(f'rating_info:{_announce.get("author_id")}')
        if not _rating:
            _rating = await self.rating_repo.get_by_id(_announce.get('author_id'))
            await self._set_to_cache(f'rating_info:{_announce.get("author_id")}', _rating)
            logger.info(f'Get author_rating <{_announce.get("author_id")}>: <{_rating}>')

        return layer_models.DetailAnnouncementResponse(
            id=_announce.get('id'),
            created=_announce.get('created'),
            modified=_announce.get('modified'),
            status=_announce.get('status').value,
            title=_announce.get('title'),
            description=_announce.get('description'),
            sub_only=_announce.get('sub_only'),
            is_free=_announce.get('is_free'),
            tickets_count=_announce.get('tickets_count'),
            tickets_left=_tickets_left,
            event_time=_announce.get('event_time'),
            event_location=_announce.get('event_location'),
            author_name=_user,
            guest_list=_guests,
            author_rating=_rating,
            movie_title=_movie.movie_title,
            duration=_movie.duration,
        )

    async def create(
        self,
        new_announce: layer_payload.APICreatePayload,
        movie_id: str | UUID,
        author_id: str | UUID,
    ) -> str | UUID:
        """
        Создание новой записи в БД.

        :param author_id: id автора
        :param movie_id: id контента
        :param new_announce: данные для создания объявления
        :return announce_id: id объявления
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        _id = str(uuid4())
        _movie = await self.movie_repo.get_by_id(movie_id)
        logger.info(f'Get movie <{movie_id}>: <{_movie}>')
        values = layer_payload.PGCreatePayload(
            id=_id,
            movie_id=movie_id,
            author_id=author_id,
            duration=_movie.duration,
            **new_announce.dict(),
        ).dict()
        query = insert(Announcement).values(**values)
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Create announcement <{_id}>')

            return _id
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError announcement <{_id}>')
            raise exc.UniqueConstraintError from ex

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.AnnouncementResponse | None]:
        """
        Получение объявлений по условию.

        :param user_id: id пользователя
        :param query: данные для фильтрации запроса к БД
        :return: список объявлений
        """
        _query = select(Announcement)
        if query.sub:
            _sub = await self.user_repo.get_subs(user_id)
            _query = _query.where(Announcement.author_id.in_(_sub))
        if query.author:
            _query = _query.filter(Announcement.author_id == query.author)
        if query.movie:
            _query = _query.filter(Announcement.movie_id == query.movie)
        if query.free:
            _query = _query.filter(Announcement.is_free == query.free)
        if query.ticket:
            _query = _query.filter(Announcement.tickets_count == query.ticket)
        if query.date:
            _query = _query.filter(Announcement.event_time == query.date)
        if query.location:
            _query = _query.filter(Announcement.event_location == query.location)

        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            logger.info(f'[-] Not found <{query}>')
            return []
        return [layer_models.AnnouncementResponse(**data) for data in scalar_result]

    async def update(
        self,
        announce_id: str | UUID,
        update_announce: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        Изменить данные в объявлении.

        :param announce_id: id объявления
        :param update_announce: данные для изменения объявления
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        query = (
            update(Announcement).where(Announcement.id == announce_id).values(update_announce.dict(exclude_none=True))
        )
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Update announcement <{announce_id}>')
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError announcement <{announce_id}>')
            raise exc.UniqueConstraintError from ex

    async def delete(self, announce_id: str | UUID) -> None:
        """
        Удаление записи из БД.

        :param announce_id: id объявления
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        _data: Announcement = await self.db.get(Announcement, announce_id)
        await self.db.delete(_data)
        await self.db.commit()
        logger.info(f'Delete announcement <{announce_id}>')


@lru_cache()
def get_announcement_repo(
    db_session: AsyncSession = Depends(get_session),
    cache: CacheProtocol = Depends(get_cache),
) -> _protocols.AnnouncementRepositoryProtocol:
    return AnnounceSqlachemyRepository(db_session, cache)
