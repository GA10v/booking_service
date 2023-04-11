from http import HTTPStatus

import pytest
from announce_data import create_payload, update_payload
from config import settings

pytestmark = pytest.mark.asyncio


async def test_create_announce(session, access_token_author):
    """Пользователь создает объявление."""
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.MOVIE}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    payload = create_payload
    async with session.post(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.OK


async def test_get_one_ok(session, access_token_author):
    """Пользователь смортрит объявление по id."""
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE_BLANK}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['status'] == 'Created'


async def test_get_one_not_found(session, access_token_author):
    """Пользователь смортрит объявление по id."""
    url = f'{settings.fastapi.service_url}/announcement/3991c6b1-940e-40da-8575-d6655e5686de'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_get_multy_0(session, access_token_author):
    """
    Пользователь смотрит все объявления.
    status == Created
    len(res) == 0
    """
    url = f'{settings.fastapi.service_url}/announcements'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 0


async def test_update_announce_ok(session, access_token_author):
    """
    Пользователь изменяет статус объявления на Alive.
    status == Alive
    """
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE_BLANK}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    payload = update_payload
    async with session.put(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['status'] == 'Alive'


async def test_get_multy_1(session, access_token_author):
    """
    Пользователь смотрит все объявления.
    status == Alive
    len(res) == 1
    """
    url = f'{settings.fastapi.service_url}/announcements'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 1


async def test_update_announce_forbidden(session, access_token_guest_2):
    """Пользователь изменяет чужое объявление."""
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_guest_2}
    payload = update_payload
    async with session.put(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_delete_announce_forbidden(session, access_token_guest_2):
    """Пользователь удаляет чужое объявление."""
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_guest_2}
    async with session.delete(url, headers=headers) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_delete_announce_ok(session, access_token_author):
    """Пользователь удаляет свое объявление."""
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE_BLANK}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.delete(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK

    _url = f'{settings.fastapi.service_url}/announcements'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(_url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 0
