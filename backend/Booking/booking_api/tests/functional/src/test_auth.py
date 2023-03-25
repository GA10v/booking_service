from http import HTTPStatus

import pytest
from config import settings

pytestmark = pytest.mark.asyncio


async def test_unauthorized(session):
    """Не авторизованный пользователь. ping"""
    url = settings.fastapi.test_ok
    async with session.post(url) as response:
        assert response.status == HTTPStatus.UNAUTHORIZED


async def test_authorized(session, access_token_moderator):
    """Авторизованный пользователь. ping"""
    url = settings.fastapi.test_ok
    headers = {'Authorization': 'Bearer ' + access_token_moderator}
    async with session.post(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
