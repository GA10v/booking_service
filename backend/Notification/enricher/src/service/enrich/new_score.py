from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientError
from models import payloads
from models.events import Event
from service.enrich.protocol import PayloadsProtocol

from core.config import settings
from core.logger import get_logger
from utils.auth import _headers

logger = get_logger(__name__)


class BaseNewScorePayload:
    def __init__(self, data: Event) -> None:
        self.data = data
        self.url_short_endpoint = settings.url_shortner.uri
        self.booking_endpoint = settings.booking.announce_uri
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self._headers = _headers()

    def get_data_to_short(self, announce_id) -> payloads.UserShortContext:
        return payloads.UserShortContext(
            user_id=self.data.context.user_id,
            created_at=datetime.now(),
            url=f'{settings.url_shortner.ANNOUNCE_URL}{announce_id}',
        )

class NewScorePayload():
    async def payload(self) -> payloads.NewScoreContext:
        try:
            pass

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            raise ex

        return payloads.NewScoreContext(
            user_name=_user.get('name'),
            author_name=_announce.get('author_name'),
            announce_title=_announce.get('title'),
            link=_link.get('url'),
        )