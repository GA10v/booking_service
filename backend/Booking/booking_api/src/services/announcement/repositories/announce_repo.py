from functools import lru_cache
from uuid import UUID, uuid4

import sqlalchemy.exc as sqlalch_exc
from fastapi import Depends
from sqlalchemy import insert, select, update

import utils.exceptions as exc
from core.logger import get_logger
from db.models.announcement import Announcement
from db.pg_db import AsyncSession, get_session
from services.announcement import layer_models, layer_payload
from services.announcement.repositories import _protocols, booking_repo, movie_repo, rating_repo, user_repo

logger = get_logger(__name__)


class AnnounceSqlachemyRepository(_protocols.AnnouncementRepositoryProtocol):
    def __init__(self, db_session: AsyncSession) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.movie_repo = movie_repo.get_movie_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        self.booking_repo = booking_repo.get_booking_repo()
        self.db = db_session
        logger.info('AnnounceSqlachemyRepository init ...')

    async def _get(self, announce_id: str | UUID) -> dict:
        """Служебный метод. Возвращает запист Announcement из БД."""
        data = await self.db.get(Announcement, announce_id)
        if data is None:
            raise exc.NotFoundError
        return data._asdict()

    async def get_by_id(self, announce_id: str | UUID) -> layer_models.DetailAnnouncementResponse:
        """Получение полной информации о Announcement"""
        query = select(Announcement).filter(Announcement.id == announce_id)
        _res = await self.db.execute(query)
        scalar_result = _res.scalars().all()
        if len(scalar_result) == 0:
            raise exc.NotFoundError
        _announce = scalar_result[0]._asdict()
        logger.debug(f'Get _res <{announce_id}>: <{_announce}>')

        _user = await self.user_repo.get_by_id(_announce.get('author_id'))
        logger.debug(f'Get user <{announce_id}>: <{_user}>')

        _movie = await self.movie_repo.get_by_id(_announce.get('movie_id'))
        logger.debug(f'Get movie <{_announce.get("movie_id")}>: <{_movie}>')

        _guests = await self.booking_repo.get_by_id(announce_id=announce_id)
        logger.debug(f'Get guest_list <{announce_id}>: <{_guests}>')
        if not _guests:
            _guests = []

        _rating = await self.rating_repo.get_by_id(_announce.get('author_id'))
        logger.debug(f'Get author_rating <{_announce.get("author_id")}>: <{_rating}>')
        if not _rating:
            _rating = 0.0

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
        """Создание новой записи в БД."""
        _id = str(uuid4())
        _movie = await self.movie_repo.get_by_id(movie_id)
        logger.debug(f'Get movie <{movie_id}>: <{_movie}>')
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
            logger.error(f'UniqueConstraintError announcement <{_id}>')
            raise exc.UniqueConstraintError from ex

    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.AnnouncementResponse | None]:
        """Получение объявлений по условию"""
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
            return []
        return [layer_models.AnnouncementResponse(**data) for data in scalar_result]

    async def update(
        self,
        announce_id: str | UUID,
        update_announce: layer_payload.APIUpdatePayload,
    ) -> None:
        """Изменить данные в объявлении"""
        query = (
            update(Announcement).where(Announcement.id == announce_id).values(update_announce.dict(exclude_none=True))
        )
        try:
            await self.db.execute(query)
            await self.db.commit()
        except sqlalch_exc.IntegrityError as ex:
            logger.error(f'UniqueConstraintError announcement <{announce_id}>')
            raise exc.UniqueConstraintError from ex

    async def delete(self, announce_id: str | UUID) -> None:
        _data: Announcement = await self.db.get(Announcement, announce_id)
        await self.db.delete(_data)
        await self.db.commit()


@lru_cache()
def get_announcement_repo(
    db_session: AsyncSession = Depends(get_session),
) -> _protocols.AnnouncementRepositoryProtocol:
    return AnnounceSqlachemyRepository(db_session)
