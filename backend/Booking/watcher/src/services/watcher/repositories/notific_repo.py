from datetime import datetime
from functools import lru_cache
from uuid import uuid4

import aiohttp
from services.watcher import layer_payload
from services.watcher.repositories import _protocols

from core.config import settings
from core.logger import get_logger
from db.redis import CacheProtocol, get_cache
from utils.auth import _headers

logger = get_logger(__name__)


class NotificApiRepository(_protocols.NotificRepositoryProtocol):
    def __init__(self, cache: CacheProtocol) -> None:
        self.notific_endpoint = f'{settings.nptific.uri}send'
        self._headers = _headers()
        self.redis = get_cache()

        logger.info('NotificApiRepository init ...')

    async def send(self, event_type: layer_payload.EventType, payload: layer_payload.DoneAnnounce) -> None:
        event = layer_payload.NotificEvent(
            notification_id=str(uuid4()),
            source_name='Watcher',
            event_type=event_type,
            context=payload.dict(),
            created_at=datetime.now(),
        ).dict()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.notific_endpoint,
                headers=self._headers,
                json=event,
            ) as resp:
                logger.info(f'Send notific <{self.notific_endpoint}>')
                logger.info(f'Send notific resp.status: <{resp.status}>')


@lru_cache()
def get_notific_repo(cache: CacheProtocol) -> _protocols.NotificRepositoryProtocol:
    return NotificApiRepository(cache)
