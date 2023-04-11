from typing import Any

from core.logger import get_logger
from db.redis import RedisCache
from services.watcher import layer_models, layer_payload
from services.watcher.repositories.notific_repo import NotificApiRepository
from services.watcher.repositories.watcher_repo import WatcherSqlachemyRepository

logger = get_logger(__name__)


class WatcherService:
    def __init__(
        self,
        repo: WatcherSqlachemyRepository,
        notific_repo: NotificApiRepository,
        cache: RedisCache,
    ) -> None:
        self.repo = repo
        self.notific_repo = notific_repo
        self.redis = cache
        logger.info('WatcherService init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def _send_notific(self, data: layer_models.UpdateStatus):
        announce = await self.repo.get_by_id(data)
        for guest in announce.guest_list:
            if guest.author_status and guest.guest_status:
                payload = layer_payload.DoneAnnounce(
                    done_announce_id=str(data.announcement_id),
                    user_id=str(guest.guest_id),
                )
                await self.notific_repo.send(event_type=layer_payload.EventType.announce_done, payload=payload)

    async def run(self) -> None:
        _data = await self.repo.get()
        if _data := await self.repo.update(_data):
            for announce in _data:
                if announce.status:
                    announce.announcement_id
                    await self._send_notific(announce)
                continue
        return
