from datetime import datetime
from typing import Union

from pydantic import BaseModel

from models.base import DeliveryType


class BaseUserContext(BaseModel):
    user_id: str
    user_name: str
    email: str
    phone_number: str | None
    telegram_name: str | None
    delivery_type: DeliveryType


class NewUserContext(BaseModel):
    user_name: str
    email: str
    link: str
    delivery_type: DeliveryType


class UserShortContext(BaseModel):
    user_id: str
    url: str
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class NewReviewsLikesContext(BaseUserContext):
    author_name: str
    announce_title: str
    guest_name: str
    link: str


class NewContentContext(BaseUserContext):
    movie_title: str


class NewPromoContext(BaseUserContext):
    text_to_promo: str


class NewAnnounceContext(BaseUserContext):
    author_name: str
    announce_title: str
    event_time: str
    movie_title: str
    link: str


class NewScoreContext(BaseUserContext):
    announcement_id: str
    author_name: str
    guest_name: str
    announce_title: str


class PutAnnounceContext(BaseUserContext):
    author_name: str
    announce_title: str
    link: str


class DeleteAnnounceContext(BaseUserContext):
    author_name: str
    announce_title: str
    link: str


class DoneAnnounceContext(BaseUserContext):
    announce_title: str
    link: str


class DeleteBookingContext(BaseUserContext):
    guest_name: str
    del_booking_announce_title: str


class NewBookingContext(BaseUserContext):
    guest_name: str
    new_booking_announce_title: str
    link: str


class StatusBookingContext(BaseUserContext):
    another_name: str
    announce_title: str
    link: str


payload = Union[
    NewUserContext,
    NewReviewsLikesContext,
    NewContentContext,
    NewPromoContext,
    NewAnnounceContext,
    PutAnnounceContext,
    DeleteAnnounceContext,
    DoneAnnounceContext,
    DeleteBookingContext,
    NewBookingContext,
    StatusBookingContext,
]
