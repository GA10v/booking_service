from http import HTTPStatus

import pytest
from announce_data import update_payload as announce_update_payload
from booking_data import multy_payload, update_payload_false, update_payload_true
from config import settings

pytestmark = pytest.mark.asyncio


async def test_update_announcement_ok(session, access_token_author):
    """
    Пользователь публикует объявление.
    status == Alive
    """
    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    payload = announce_update_payload
    async with session.put(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['status'] == 'Alive'


async def test_add_booking_forbidden(session, access_token_author):
    """Пользователь отправляет запрос на свое событие."""
    url = f'{settings.fastapi.service_url}/booking/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.post(url, headers=headers) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_add_booking_ok(session, access_token_user):
    """Пользователь отправляет запрос на событие."""
    url = f'{settings.fastapi.service_url}/booking/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_user}
    async with session.post(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK


async def test_get_booking_by_id_ok(session, access_token_guest_1):
    """Пользователь получает подробную информацию о своей заявке."""
    url = f'{settings.fastapi.service_url}/booking/{settings.data.BOOKING_G1}'
    headers = {'Authorization': 'Bearer ' + access_token_guest_1}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK


async def test_get_booking_by_id_forbidden(session, access_token_guest_1):
    """Пользователь получает подробную информацию о чужой заявке."""
    url = f'{settings.fastapi.service_url}/booking/{settings.data.BOOKING_G2}'
    headers = {'Authorization': 'Bearer ' + access_token_guest_1}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_accept_booking_ok(session, access_token_author):
    """
    Автор принимает запрос на событие.
    Свободные места закываются tickets_left == 0.
    Статус объявления меняется на Closed.
    """
    url = f'{settings.fastapi.service_url}/booking/{settings.data.BOOKING_G2}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    payload = update_payload_true
    async with session.put(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.OK

    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['tickets_left'] == 0
        assert body['status'] == 'Closed'


async def test_decline_booking_ok(session, access_token_author):
    """
    Автор отклоняет запрос на событие.
    Свободные места появляются tickets_left == 1.
    Статус объявления меняется на Alive.

    """
    url = f'{settings.fastapi.service_url}/booking/{settings.data.BOOKING_G2}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    payload = update_payload_false
    async with session.put(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.OK

    url = f'{settings.fastapi.service_url}/announcement/{settings.data.ANNOUNCE}'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['tickets_left'] == 1
        assert body['status'] == 'Alive'


async def test_get_all_booking_as_author(session, access_token_author):
    """Пользователь получает все заявки на событие, как автор."""
    url = f'{settings.fastapi.service_url}/bookings'
    headers = {'Authorization': 'Bearer ' + access_token_author}
    payload = multy_payload
    async with session.get(url, headers=headers, json=payload) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 3
