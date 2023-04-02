from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MovieToResponse(BaseModel):
    movie_title: str


class RatingToResponse(BaseModel):
    user_raring: float


class UserToResponse(BaseModel):
    user_name: str


class AnnounceToResponse(BaseModel):
    author_id: str | UUID
    event_time: datetime


class BookingResponse(BaseModel):
    id: str | UUID
    guest_name: str
    author_status: bool
    guest_status: bool
    guest_rating: float


class DetailBookingResponse(BaseModel):
    id: str | UUID
    announcement_id: str | UUID
    movie_title: str
    author_name: str
    guest_name: str
    author_status: bool | None = None
    guest_status: bool = True
    guest_rating: float
    author_rating: float
    event_time: datetime


class PGBooking(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
    announcement_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    author_status: bool | None
    guest_status: bool | None
    event_time: datetime
