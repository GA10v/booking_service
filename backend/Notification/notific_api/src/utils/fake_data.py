from datetime import datetime
from uuid import uuid4

from faker import Faker

from core.config import settings
from models import context
from models.base import EventType
from models.events import Event

fake = Faker()


def _get_user() -> context.NewUser:
    if settings.debug:
        return context.NewUser(
            user_id=str(uuid4()),
            name=fake.first_name(),
            email=settings.debug.TEST_EMAIL[0],
        ).dict()
    return context.NewUser(
        user_id=str(uuid4()),
        name=fake.first_name(),
        email=fake.email(),
    ).dict()


def _get_likes() -> context.NewReviewsLikes:
    return context.NewReviewsLikes(
        author_id='50760ee6-2073-445d-ad25-f665937f3b33',
        guest_id='d0c5635c-3211-4cf8-94ab-cbe6800771c4',
        announcement_id='eca370e7-c65d-44f3-b390-5c2733df02e6',
    ).dict()


def _get_content() -> context.NewContent:
    return context.NewContent(
        user_id=str(uuid4()),
        movie_id=str(uuid4()),
    ).dict()


def _get_promo() -> context.NewPromo:
    return context.NewPromo(
        user_id=str(uuid4()),
        text_to_promo='TEXT TEXT TEXT TEXT',
    ).dict()


def _get_new_announce() -> context.NewAnnounce:
    return context.NewAnnounce(
        user_id=str(uuid4()),
        new_announce_id=settings.booking.FAKE_ANNOUNCE,
    ).dict()


def _get_put_announce() -> context.PutAnnounce:
    return context.PutAnnounce(
        put_announce_id=settings.booking.FAKE_ANNOUNCE,
        user_id=str(uuid4()),
    ).dict()


def _get_delete_announce() -> context.DeleteAnnounce:
    return context.DeleteAnnounce(
        delete_announce_id=str(uuid4()),
        author_name='Author Author',
        announce_title='Fake delete title',
        user_id=str(uuid4()),
    ).dict()


def _get_done_announce() -> context.DoneAnnounce:
    return context.DoneAnnounce(
        done_announce_id=settings.booking.FAKE_ANNOUNCE,
        user_id=str(uuid4()),
    ).dict()


def _get_delete_booking() -> context.DeleteBooking:
    return context.DeleteBooking(
        del_booking_announce_id=settings.booking.FAKE_ANNOUNCE,
        guest_name='Guest Guest',
        user_id=str(uuid4()),
    ).dict()


def _get_new_booking() -> context.NewBooking:
    return context.NewBooking(
        new_booking_id=settings.booking.FAKE_BOOKING,
        announce_id=settings.booking.FAKE_ANNOUNCE,
        user_id=str(uuid4()),
    ).dict()


def _get_status_booking() -> context.StatusBooking:
    return context.StatusBooking(
        status_booking_id=settings.booking.FAKE_BOOKING,
        announce_id=settings.booking.FAKE_ANNOUNCE,
        user_id=str(uuid4()),
        another_id=str(uuid4()),
    ).dict()


def get_user_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Auth',
        event_type=EventType.welcome,
        context=context.NewUser(**_get_user()),
        created_at=datetime.now(),
    )


def get_likes_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Generator',
        event_type=EventType.new_likes,
        context=context.NewReviewsLikes(**_get_likes()),
        created_at=datetime.now(),
    )


def get_content_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Generator',
        event_type=EventType.new_content,
        context=context.NewContent(**_get_content()),
        created_at=datetime.now(),
    )


def get_promo_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Generator',
        event_type=EventType.promo,
        context=context.NewPromo(**_get_promo()),
        created_at=datetime.now(),
    )


def get_new_announce_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.announce_new,
        context=context.NewAnnounce(**_get_new_announce()),
        created_at=datetime.now(),
    )


def get_put_announce_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.announce_put,
        context=context.PutAnnounce(**_get_put_announce()),
        created_at=datetime.now(),
    )


def get_delete_announce_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.announce_delete,
        context=context.DeleteAnnounce(**_get_delete_announce()),
        created_at=datetime.now(),
    )


def get_done_announce_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.announce_done,
        context=context.DoneAnnounce(**_get_done_announce()),
        created_at=datetime.now(),
    )


def get_delete_booking_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.booking_delete,
        context=context.DeleteBooking(**_get_delete_booking()),
        created_at=datetime.now(),
    )


def get_new_booking_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.booking_new,
        context=context.NewBooking(**_get_new_booking()),
        created_at=datetime.now(),
    )


def get_status_booking_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Booking',
        event_type=EventType.booking_status,
        context=context.StatusBooking(**_get_status_booking()),
        created_at=datetime.now(),
    )
