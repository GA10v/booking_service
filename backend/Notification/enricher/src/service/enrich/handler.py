from models.base import EventType
from models.events import Event
from models.payloads import payload
from service.enrich.new_content import NewContentPayloads
from service.enrich.new_promo import NewPromoPayloads
from service.enrich.new_review_likes import NewReviewLikesPayloads
from service.enrich.new_user import NewUserPayload

from core.logger import get_logger

logger = get_logger(__name__)


async def get_payload(data: Event) -> payload:
    logger.info('Get payload...')
    if data.event_type == EventType.welcome:
        payload = NewUserPayload(data)
    elif data.event_type == EventType.new_content:
        payload = NewContentPayloads(data)
    elif data.event_type == EventType.new_likes:
        payload = NewReviewLikesPayloads(data)
    elif data.event_type == EventType.promo:
        payload = NewPromoPayloads(data)

    return await payload.payload()
