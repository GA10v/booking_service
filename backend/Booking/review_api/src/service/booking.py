import logging
from functools import lru_cache

import httpx

from src.core.config import settings
from src.models.announce import AnnouncementToReviewResponse
from src.utils.auth import _headers

logger = logging.getLogger(__name__)


class BookingService:
    def __init__(self):
        self.base_url = f'{settings.fastapi.uri}/announcement'

    async def get_booking(self, announcement_id: str, guest_id: str) -> AnnouncementToReviewResponse:
        url = f'{self.base_url}/{announcement_id}/{guest_id}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=_headers())
        logger.info(f'Booking: {response}')
        result = None
        if response.json():
            result = AnnouncementToReviewResponse.parse_obj(response.json())
        return result


@lru_cache()
def get_booking_service() -> BookingService:
    return BookingService()
