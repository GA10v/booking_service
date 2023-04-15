from datetime import datetime
from functools import lru_cache
from uuid import uuid4

import aiohttp

from src.core.config import settings
from src.core.logger import get_logger
from src.models import noitifciations
from src.models.noitifciations import EventType
from src.service.base import NoificationServiceBase
from src.utils.auth import _headers

logger = get_logger(__name__)


class NotificApiRepository(NoificationServiceBase):
    def __init__(self) -> None:
        self.notific_endpoint = f'{settings.notific.uri}send'
        self._headers = _headers()

    async def send(self, payload: noitifciations.NewReviewsLikes) -> None:
        event_type = EventType.new_likes
        event = noitifciations.NotificEvent(
            notification_id=str(uuid4()),
            source_name='Review service',
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
def get_notific_repo() -> NoificationServiceBase:
    return NotificApiRepository()
