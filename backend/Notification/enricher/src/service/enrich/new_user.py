from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientError
from models.events import Event
from models.payloads import NewUserContext, UserShortContext
from service.enrich.protocol import PayloadsProtocol
from utils.auth import _headers

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class NewUserPayload(PayloadsProtocol):
    def __init__(self, data: Event) -> None:
        self.data = data
        self.url_short_endpoint = settings.url_shortner.uri
        self._headers = _headers()

    def get_data_to_short(self):
        return UserShortContext(
            user_id=self.data.context.user_id,
            created_at=datetime.now(),
            url=settings.url_shortner.REDIRECT_URL,
        )

    async def payload(self) -> NewUserContext:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short().dict(),
                ) as resp:
                    _link = await resp.json()
        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            raise ex
        return NewUserContext(
            user_name=self.data.context.name,
            email=self.data.context.email,
            link=_link.get('url'),
            delivery_type='email',
        )
