from typing import Union
from uuid import UUID

from pydantic import BaseModel


class NewUser(BaseModel):
    user_id: str
    name: str
    email: str


class NewReviewsLikes(BaseModel):
    review_id: str
    author_id: str
    movie_id: str
    likes: int


class NewContent(BaseModel):
    user_id: str
    movie_id: str


class NewPromo(BaseModel):  # TODO узнать что будет приходить от админки
    user_id: str
    text_to_promo: str


class NewAnnounce(BaseModel):
    new_announce_id: str | UUID
    user_id: str | UUID


class NewScore(BaseModel):
    announce_id: str | UUID
    author_id: str | UUID


class PutAnnounce(BaseModel):
    put_announce_id: str | UUID
    user_id: str | UUID


class DeleteAnnounce(BaseModel):
    delete_announce_id: str | UUID
    author_name: str
    announce_title: str
    user_id: str | UUID


class DoneAnnounce(BaseModel):
    done_announce_id: str | UUID
    user_id: str | UUID


class DeleteBooking(BaseModel):
    del_booking_announce_id: str | UUID
    guest_name: str
    user_id: str | UUID


class NewBooking(BaseModel):
    new_booking_id: str | UUID
    announce_id: str | UUID
    user_id: str | UUID


class StatusBooking(BaseModel):
    status_booking_id: str | UUID
    another_id: str | UUID
    announce_id: str | UUID
    user_id: str | UUID


context = Union[
    NewUser,
    NewReviewsLikes,
    NewAnnounce,
    PutAnnounce,
    DeleteAnnounce,
    NewContent,
    NewPromo,
    DoneAnnounce,
    DeleteBooking,
    NewBooking,
    StatusBooking,
]
