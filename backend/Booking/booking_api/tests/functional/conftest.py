import asyncio

import aiohttp
import jwt
import pytest_asyncio
from config import settings


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
def access_token_moderator():
    data = {'sub': settings.data.SUDO, 'permissions': [0, 3], 'is_super': True}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)


@pytest_asyncio.fixture(scope='session')
def access_token_user():
    data = {'sub': settings.data.USER, 'permissions': [0, 1], 'is_super': False}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)


@pytest_asyncio.fixture(scope='session')
def access_token_author():
    data = {'sub': settings.data.AUTHOR, 'permissions': [0, 1], 'is_super': False}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)


@pytest_asyncio.fixture(scope='session')
def access_token_guest_1():
    data = {'sub': settings.data.GUEST_1, 'permissions': [0, 1], 'is_super': False}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)


@pytest_asyncio.fixture(scope='session')
def access_token_guest_2():
    data = {'sub': settings.data.GUEST_2, 'permissions': [0, 1], 'is_super': False}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
