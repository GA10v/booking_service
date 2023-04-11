from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

import aiohttp
import pytz
import sqlalchemy.exc as sqlalch_exc
from aiohttp.client_exceptions import ClientError
from services.watcher import layer_models, layer_payload
from services.watcher.repositories import _protocols
from sqlalchemy import select, update

from core.config import settings
from core.logger import get_logger
from db.db import AsyncSession
from db.models.announcement import Announcement
from db.redis import CacheProtocol
from utils.auth import _headers

logger = get_logger(__name__)
utc = pytz.UTC


class WatcherSqlachemyRepository(_protocols.WatcherRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: CacheProtocol) -> None:
        self.db = db_session
        self.redis = cache
        self.announce_endpoint = settings.booking.announce_uri
        self._headers = _headers()
        logger.info('WatcherSqlachemyRepository init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    @staticmethod
    def _check_time(start_time: datetime, duration: int) -> bool:
        now = datetime.utcnow()
        end_time = start_time + timedelta(minutes=duration)
        if end_time < utc.localize(now):
            return True
        return

    async def get(self) -> list[str | UUID]:
        now = datetime.utcnow()
        query = (
            select(Announcement)
            .where(Announcement.event_time < utc.localize(now))
            .filter(Announcement.status == layer_payload.EventStatus.Alive.value)
        )

        _res = await self.db.execute(query)
        scalar_result = [data._asdict() for data in _res.scalars().all()]
        if len(scalar_result) == 0:
            return []
        return [data.get('id') for data in scalar_result]

    async def update(self, data: list[str | UUID]) -> list[layer_models.UpdateStatus]:
        res = []
        for announce_id in data:
            _data = await self.db.get(Announcement, announce_id)
            _announcement = _data._asdict()

            if self._check_time(
                start_time=_announcement.get('event_time'),
                duration=_announcement.get('duration'),
            ):
                query = (
                    update(Announcement)
                    .where(Announcement.id == announce_id)
                    .values({'status': layer_payload.EventStatus.Done.value})
                )
                try:
                    await self.db.execute(query)
                    await self.db.commit()
                    logger.info(f'Update Event <{announce_id}>')
                    res.append(
                        layer_models.UpdateStatus(
                            announcement_id=announce_id,
                            status=True,
                        ),
                    )
                except sqlalch_exc.IntegrityError:
                    res.append(
                        layer_models.UpdateStatus(
                            announcement_id=announce_id,
                            status=False,
                        ),
                    )
        return res

    async def get_by_id(self, data: layer_models.UpdateStatus) -> layer_models.DetailAnnouncementResponse:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.announce_endpoint}{data.announcement_id}',
                    headers=self._headers,
                ) as resp:
                    _announce = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            raise ex

        return layer_models.DetailAnnouncementResponse(**_announce)


def get_watcher_repo(
    db_session: AsyncSession,
    cache: CacheProtocol,
) -> _protocols.WatcherRepositoryProtocol:
    return WatcherSqlachemyRepository(db_session, cache)
