from http import HTTPStatus

import pytest
from config import settings

pytestmark = pytest.mark.asyncio


async def test_ping(session, access_token_moderator):
    """Проверка api 200."""
    url = settings.fastapi.test_ok
    headers = {'Authorization': 'Bearer ' + access_token_moderator}
    async with session.post(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
