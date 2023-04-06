from datetime import datetime
from random import randint
from uuid import uuid4

from faker import Faker
from models.base import EventType
from models.context import NewContent, NewPromo, NewReviewsLikes, NewUser
from models.events import Event

from core.config import settings

fake = Faker()


def _get_user() -> NewUser:
    if settings.debug:
        return NewUser(
            user_id=str(uuid4()),
            name=fake.first_name(),
            email=settings.debug.TEST_EMAIL[0],
        ).dict()
    return NewUser(
        user_id=str(uuid4()),
        name=fake.first_name(),
        email=fake.email(),
    ).dict()


def _get_likes() -> NewReviewsLikes:
    return NewReviewsLikes(
        review_id=str(uuid4()),
        author_id=str(uuid4()),
        movie_id=str(uuid4()),
        likes=randint(0, 50),
    ).dict()


def _get_content() -> NewContent:
    return NewContent(
        user_id=str(uuid4()),
        movie_id=str(uuid4()),
    ).dict()


def _get_promo() -> NewPromo:
    return NewPromo(
        user_id=str(uuid4()),
        text_to_promo='TEXT TEXT TEXT TEXT',
    ).dict()


def get_user_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Auth',
        event_type=EventType.welcome,
        context=NewUser(**_get_user()),
        created_at=datetime.now(),
    )


def get_likes_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Generator',
        event_type=EventType.new_likes,
        context=NewReviewsLikes(**_get_likes()),
        created_at=datetime.now(),
    )


def get_content_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Generator',
        event_type=EventType.new_content,
        context=NewContent(**_get_content()),
        created_at=datetime.now(),
    )


def get_promo_event() -> Event:
    return Event(
        notification_id=str(uuid4()),
        source_name='Generator',
        event_type=EventType.promo,
        context=NewPromo(**_get_promo()),
        created_at=datetime.now(),
    )
