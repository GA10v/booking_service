import json
from functools import lru_cache
from uuid import uuid4

import jwt
import httpx
import logging

from core.config import settings
from models.booking import PGBooking

logger = logging.getLogger(__name__)


def _headers() -> str:
    data = {
        'sub': str(uuid4()),
        'permissions': [0, 3],
        'is_super': True,
    }
    access_token = jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)
    return {'Authorization': 'Bearer ' + access_token}


class BookingService:

    def __init__(self):
        self.base_url = f'http://{settings.fastapi.HOST}:{settings.fastapi.PORT}/{settings.fastapi.API_PREFIX}/booking'

    async def get_booking(self, booking_id: str):
        url = f'{self.base_url}/{booking_id}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=_headers())
        logger.info(f'Response: {response.text} status {response.status_code}')
        result = None
        if response.json():
            result = PGBooking(json.loads(response.json()))

        return result


@lru_cache()
def get_booking_service() -> BookingService:
    return BookingService()
