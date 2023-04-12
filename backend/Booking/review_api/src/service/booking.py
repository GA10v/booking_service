import json
import logging
from functools import lru_cache
from uuid import uuid4

import httpx
import jwt

from src.core.config import settings
from src.models.announce import AnnouncementToReviewResponse

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
        self.base_url = (
            f'http://{settings.fastapi.HOST}:{settings.fastapi.PORT}/' f'{settings.fastapi.API_PREFIX}/announcement'
        )

    async def get_booking(self, announcement_id: str, guest_id: str) -> AnnouncementToReviewResponse:
        url = f'{self.base_url}/{announcement_id}/{guest_id}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=_headers())
        logger.info(f'Response: {response.text} status {response.status_code}')
        result = None
        if response.json():
            result = AnnouncementToReviewResponse(json.loads(response.json()))

        return result


@lru_cache()
def get_booking_service() -> BookingService:
    return BookingService()
