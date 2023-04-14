from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientError

from core.config import settings
from core.logger import get_logger
from models import payloads
from models.events import Event
from models.payloads import NewReviewsLikesContext
from service.enrich.protocol import PayloadsProtocol
from utils.auth import _headers

logger = get_logger(__name__)


class NewReviewLikesPayloads(PayloadsProtocol):
    def __init__(self, data: Event) -> None:
        self.data = data
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self.booking_endpoint = settings.booking.announce_uri
        self.url_short_endpoint = settings.url_shortner.uri
        self._headers = _headers()

    def get_data_to_short(self, announce_id) -> payloads.UserShortContext:
        return payloads.UserShortContext(
            user_id=self.data.context.author_id,
            created_at=datetime.now(),
            url=f'{settings.url_shortner.REVIEW_URL}{announce_id}',
        )

    async def payload(self) -> NewReviewsLikesContext:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.author_id}',
                    headers=self._headers,
                ) as resp:
                    _author = await resp.json()

                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.guest_id}',
                    headers=self._headers,
                ) as resp:
                    _guest = await resp.json()

                async with session.get(
                    f'{self.booking_endpoint}{self.data.context.announcement_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short(announce_id=self.data.context.announcement_id).dict(),
                ) as resp:
                    _link = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return NewReviewsLikesContext(
            user_id=_author.get('user_id'),
            user_name=_author.get('name'),
            email=_author.get('email'),
            phone_number=_author.get('phone_number'),
            telegram_name=_author.get('telegram_name'),
            delivery_type=_author.get('delivery_type'),
            author_name=_author.get('name'),
            announce_title=_announce.get('title'),
            guest_name=_guest.get('name'),
            link=_link.get('url'),
        )
