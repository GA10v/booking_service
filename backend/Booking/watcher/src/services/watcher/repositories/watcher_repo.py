from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

import pytz
import sqlalchemy.exc as sqlalch_exc
from core.logger import get_logger
from db.db import AsyncSession
from db.models.announcement import Announcement
from db.redis import RedisCache
from services.watcher import layer_models, layer_payload
from services.watcher.repositories import _protocols
from sqlalchemy import select, update

logger = get_logger(__name__)
utc = pytz.UTC


class WatcherSqlachemyRepository(_protocols.WatcherRepositoryProtocol):
    def __init__(self, db_session: AsyncSession, cache: RedisCache) -> None:
        self.db = db_session
        self.redis = cache
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


def get_watcher_repo(
    db_session: AsyncSession,
    cache: RedisCache,
) -> _protocols.WatcherRepositoryProtocol:
    return WatcherSqlachemyRepository(db_session, cache)
