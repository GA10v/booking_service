from functools import lru_cache
from uuid import UUID

import aiohttp
from aiohttp.client_exceptions import ClientError

from core.config import settings
from core.logger import get_logger
from services.announcement.repositories import _protocols
from utils.auth import _headers

logger = get_logger(__name__)


class UserMockRepository(_protocols.UserRepositoryProtocol):
    def __init__(self) -> None:
        self.auth_endpoint = f'{settings.auth.uri}user_info/'
        self.ugc_endpoint = f'{settings.ugc.uri}subscribers/'
        self._headers = _headers()

        logger.info('UserMockRepository init ...')

    async def get_by_id(self, user_id: str | UUID) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.auth_endpoint}{user_id}',
                    headers=self._headers,
                ) as resp:
                    _user = await resp.json()
                    logger.debug(f'Get user <{user_id}>: <{_user}>')

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return f"{_user.get('name')} {_user.get('last_name')}"

    async def get_subs(self, user_id: str | UUID) -> list[str | UUID]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.ugc_endpoint}{user_id}',
                    headers=self._headers,
                ) as resp:
                    _subs = await resp.json()
                    logger.debug(f'Get subs for user <{user_id}>: <{_subs}>')

        except ClientError as ex:  # noqa: F841
            logger.debug(f'Except <{ex}>')
            return None

        return _subs


@lru_cache()
def get_user_repo() -> _protocols.UserRepositoryProtocol:
    return UserMockRepository()
