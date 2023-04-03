from functools import lru_cache
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy.exc as sqlalch_exc
from fastapi import Depends
from sqlalchemy import insert, select, update

import utils.exceptions as exc
from core.logger import get_logger
from db.models.booking import Booking
from db.pg_db import AsyncSession, get_session
from db.redis import CacheProtocol, RedisCache, get_cache
from services.booking import layer_models, layer_payload
from services.booking.repositories import _protocols, announce_repo, movie_repo, rating_repo, user_repo

logger = get_logger(__name__)


class BookingSqlachemyRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: RedisCache) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.movie_repo = movie_repo.get_movie_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.announce_repo = announce_repo.get_announcement_repo()
        self.db = db_session
        self.redis = cache
        logger.info('BookingSqlachemyRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _get(self, booking_id: str | UUID) -> layer_models.PGBooking:
        """
        Служебный метод. Возвращает запись Booking из БД.

        :param booking_id: id заявки
        :return: dict данные из БД по id
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        data = await self.db.get(Booking, booking_id)
        if data is None:
            logger.info(f'[-] Not found <{booking_id}>')
            raise exc.NotFoundError
        return layer_models.PGBooking(**data._asdict())

    async def _get_booking_resp(self, data: dict[str, Any]) -> layer_models.BookingResponse:
        """
        Служебный метод. Возвращает BookingResponse.

        :param data: сырые данные из БД
        :return: BookingResponse
        """
        _booking = layer_models.PGBooking(**data)

        _author = await self.user_repo.get_by_id(_booking.author_id)
        logger.info(f'Get user <{_booking.author_id}>: <{_author}>')

        _guest = await self.user_repo.get_by_id(_booking.guest_id)
        logger.info(f'Get user <{_booking.guest_id}>: <{_guest}>')

        return layer_models.BookingResponse(
            id=_booking.id,
            author_name=_author.user_name,
            guest_name=_guest.user_name,
            author_status=_booking.author_status,
            guest_status=_booking.guest_status,
        )

    async def get_by_id(self, booking_id: str | UUID) -> layer_models.DetailBookingResponse:
        """Получение полной информации о Booking.

        :param booking_id: id заявки
        :return: подробная информация о заявке
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        try:
            _booking = await self._get(booking_id)
        except exc.NotFoundError:
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
        )

    async def create(self, announce_id: str | UUID, user_id: str | UUID) -> str | UUID:
        """Создание новой записи в БД.

        :param announce_id: id объявления
        :param user_id: id гостя
        :return booking_id: id заявки
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        booking_id = str(uuid4())

        _announce: layer_models.AnnounceToResponse = self.announce_repo.get_by_id(announce_id)
        logger.info(f'Get announcement <{announce_id}>: <{_announce}>')

        values = layer_payload.PGCreatePayload(
            id=booking_id,
            announcement_id=announce_id,
            movie_id=_announce.movie_id,
            author_id=_announce.author_id,
            guest_id=user_id,
            event_time=_announce.event_time,
        ).dict()
        query = insert(Booking).values(**values)
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Create booking <{booking_id}>')

            return booking_id
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError booking <{booking_id}>')
            raise exc.UniqueConstraintError from ex

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.BookingResponse]:
        """Получение заявок по условию.

        :param user_id: id пользователя
        :param query: данные для фильтрации запроса к БД
        :return: список заявок
        """
        _query = select(Booking)
        if query.is_self:
            _query = _query.filter(Booking.author_id == user_id)
        if query.author:
            _query = _query.filter(Booking.author_id == query.author)
        if query.movie:
            _query = _query.filter(Booking.movie_id == query.movie)
        if query.date:
            _query = _query.filter(Booking.event_time == query.date)

        _res = await self.db.execute(_query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]

        if len(scalar_result) == 0:
            logger.info(f'[-] Not found <{query}>')
            return []
        return [self._get_booking_resp(**data) for data in scalar_result]

    async def delete(self, booking_id: str | UUID) -> None:
        """
        Удаление записи из БД.

        :param announce_id: id заявки
        :raises NotFoundError: если указаная запись не была найдена в базе
        """
        _data: Booking = await self.db.get(Booking, booking_id)
        await self.db.delete(_data)
        await self.db.commit()
        logger.info(f'Delete booking <{booking_id}>')

    async def update(
        self,
        user_id: str | UUID,
        booking_id: str | UUID,
        new_status: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        Изменить свой статус в заявке.

        :param booking_id: id заявки
        :param new_status: новый статус
        :raises NotFoundError: если указаная запись не была найдена в базе
        :raises UniqueConstraintError: если запист уже существует в базе
        """
        query = update(Booking).where(Booking.id == booking_id)
        booking: layer_models.PGBooking = await self._get(booking_id)
        if user_id == str(booking.author_id):
            if new_status.my_status == booking.author_status:
                return
            query = query.values(
                {'author_status': new_status.my_status},
            )
        elif user_id == str(booking.guest_id):
            if new_status.my_status == booking.guest_status:
                return
            query = query.values(
                {'guest_status': new_status.my_status},
            )
        try:
            await self.db.execute(query)
            await self.db.commit()
            logger.info(f'Update booking <{booking_id}>')
        except sqlalch_exc.IntegrityError as ex:
            logger.info(f'UniqueConstraintError booking <{booking_id}>')
            raise exc.UniqueConstraintError from ex


@lru_cache()
def get_booking_repo(
    db_session: AsyncSession = Depends(get_session),
    cache: CacheProtocol = Depends(get_cache),
) -> _protocols.BookingRepositoryProtocol:
    return BookingSqlachemyRepository(db_session, cache)
