from core.logger import get_logger
from models.base import EventType
from models.events import Event
from models.payloads import payload
from service.enrich import announce, booking, new_content, new_promo, new_review_likes, new_user, new_score

logger = get_logger(__name__)


async def get_payload(data: Event) -> payload:
    logger.info('Get payload...')
    if data.event_type == EventType.welcome:
        payload = new_user.NewUserPayload(data)
    elif data.event_type == EventType.new_content:
        payload = new_content.NewContentPayloads(data)
    elif data.event_type == EventType.new_likes:
        payload = new_review_likes.NewReviewLikesPayloads(data)
    elif data.event_type == EventType.promo:
        payload = new_promo.NewPromoPayloads(data)
    elif data.event_type == EventType.announce_new:
        payload = announce.NewAnnouncementPayload(data)
    elif data.event_type == EventType.announce_put:
        payload = announce.PutAnnouncementPayload(data)
    elif data.event_type == EventType.announce_delete:
        payload = announce.DeleteAnnouncementPayload(data)
    elif data.event_type == EventType.announce_done:
        payload = announce.DoneAnnouncementPayload(data)
    elif data.event_type == EventType.booking_delete:
        payload = booking.DeleteBookingPayload(data)
    elif data.event_type == EventType.booking_status:
        payload = booking.StatusBookingPayload(data)
    elif data.event_type == EventType.booking_new:
        payload = booking.NewBookingPayload(data)
    elif data.event_type == EventType.new_score:
        payload = new_score.NewScorePayload(data)
    return await payload.payload()
