from datetime import datetime

import aiohttp
from aiohttp.client_exceptions import ClientError

from core.config import settings
from core.logger import get_logger
from models import payloads
from models.events import Event
from service.enrich.protocol import PayloadsProtocol
from utils.auth import _headers

logger = get_logger(__name__)


class BaseBookingPayload:
    def __init__(self, data: Event) -> None:
        self.data = data
        self.url_short_endpoint = settings.url_shortner.uri
        self.announce_endpoint = settings.booking.announce_uri
        self.booking_endpoint = settings.booking.booking_uri
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self._headers = _headers()

    def get_data_to_short(self, booking_id) -> payloads.UserShortContext:
        return payloads.UserShortContext(
            user_id=self.data.context.user_id,
            created_at=datetime.now(),
            url=f'{settings.url_shortner.BOOKING_URL}{booking_id}',
        )


class DeleteBookingPayload(PayloadsProtocol, BaseBookingPayload):
    async def payload(self) -> payloads.DeleteBookingContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.announce_endpoint}{self.data.context.del_booking_announce_id}',
                    headers=self._headers,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.user_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            raise ex

        return payloads.DeleteBookingContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            guest_name=self.data.context.guest_name,
            del_booking_announce_title=_announce.get('title'),
        )


class NewBookingPayload(PayloadsProtocol, BaseBookingPayload):
    async def payload(self) -> payloads.NewBookingContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.booking_endpoint}{self.data.context.new_booking_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _booking = await resp.json()

                async with session.get(
                    f'{self.announce_endpoint}{self.data.context.announce_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short(self.data.context.new_booking_id).dict(),
                ) as resp:
                    _link = await resp.json()

                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.user_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            raise ex

        return payloads.NewBookingContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            guest_name=_booking.get('guest_name'),
            new_booking_announce_title=_announce.get('title'),
            link=_link.get('url'),
        )


class StatusBookingPayload(PayloadsProtocol, BaseBookingPayload):
    async def payload(self) -> payloads.StatusBookingContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.announce_endpoint}{self.data.context.announce_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short(self.data.context.status_booking_id).dict(),
                ) as resp:
                    _link = await resp.json()

                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.user_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()

                async with session.post(
                    f'{self.auth_endpoint}{self.data.context.user_id}',
                    headers=self._headers,
                ) as resp:
                    _another = await resp.json()

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            raise ex

        return payloads.StatusBookingContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            another_name=_another.get('name'),
            announce_title=_announce.get('title'),
            link=_link.get('url'),
        )
