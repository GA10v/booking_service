from http import HTTPStatus

import pytest
from config import settings

pytestmark = pytest.mark.asyncio


async def test_ping(session):
    """Проверка api 200."""
    url = settings.fastapi.test_ok
    async with session.post(url) as response:
        assert response.status == HTTPStatus.OK
