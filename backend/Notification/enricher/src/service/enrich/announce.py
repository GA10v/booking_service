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


class BaseAnnouncementPayload:
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


class NewAnnouncementPayload(PayloadsProtocol, BaseAnnouncementPayload):
    async def payload(self) -> payloads.NewAnnounceContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.booking_endpoint}{self.data.context.new_announce_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short(announce_id=self.data.context.new_announce_id).dict(),
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

        return payloads.NewAnnounceContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            author_name=_announce.get('author_name'),
            announce_title=_announce.get('title'),
            event_time=_announce.get('event_time'),
            movie_title=_announce.get('movie_title'),
            link=_link.get('url'),
        )


class PutAnnouncementPayload(PayloadsProtocol, BaseAnnouncementPayload):
    async def payload(self) -> payloads.PutAnnounceContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.booking_endpoint}{self.data.context.put_announce_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short(announce_id=self.data.context.put_announce_id).dict(),
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

        return payloads.PutAnnounceContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            author_name=_announce.get('author_name'),
            announce_title=_announce.get('title'),
            link=_link.get('url'),
        )


class DeleteAnnouncementPayload(PayloadsProtocol, BaseAnnouncementPayload):
    def get_data_to_short(self) -> payloads.UserShortContext:
        return payloads.UserShortContext(
            user_id=self.data.context.user_id,
            created_at=datetime.now(),
            url=settings.url_shortner.ALL_ANNOUNCE_URL,
        )

    async def payload(self) -> payloads.DeleteAnnounceContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short().dict(),
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

        return payloads.DeleteAnnounceContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            author_name=self.data.context.author_name,
            announce_title=self.data.context.author_name,
            link=_link.get('url'),
        )


class DoneAnnouncementPayload(PayloadsProtocol, BaseAnnouncementPayload):
    def get_data_to_short(self) -> payloads.UserShortContext:
        return payloads.UserShortContext(
            user_id=self.data.context.user_id,
            created_at=datetime.now(),
            url=settings.url_shortner.RATING_URL,  # TODO: Информация от Павла
        )

    async def payload(self) -> payloads.DoneAnnounceContext:
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(
                    f'{self.booking_endpoint}{self.data.context.done_announce_id}',
                    headers=self._headers,
                    ssl=False,
                ) as resp:
                    _announce = await resp.json()

                async with session.post(
                    self.url_short_endpoint,
                    headers=self._headers,
                    json=self.get_data_to_short().dict(),  # TODO Информация от Павла
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

        return payloads.DoneAnnounceContext(
            user_id=_user.get('user_id'),
            user_name=_user.get('name'),
            email=_user.get('email'),
            phone_number=_user.get('phone_number'),
            telegram_name=_user.get('telegram_name'),
            delivery_type=_user.get('delivery_type'),
            announce_title=_announce.get('title'),
            link=_link.get('url'),
        )
