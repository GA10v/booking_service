from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.base import DefaultModel


class PGBooking(DefaultModel):
    announcement_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    author_status: bool | None = None
    guest_status: bool
    event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['announcement_id'] = str(_dict['announcement_id'])
        _dict['author_id'] = str(_dict['author_id'])
        _dict['guest_id'] = str(_dict['guest_id'])
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class BookingResponse(BaseModel):
    booking_id: str | UUID
    guest_name: str
    author_status: bool
    guest_status: bool
    guest_rating: float

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['booking_id'] = str(_dict['booking_id'])
        return _dict


class DetailBookingResponse(BaseModel):
    booking_id: str | UUID
    announcement_id: str | UUID
    movie_title: str
    author_name: str
    guest_name: str
    author_status: bool | None
    guest_status: bool
    guest_rating: float
    author_rating: float
    event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['booking_id'] = str(_dict['booking_id'])
        _dict['announcement_id'] = str(_dict['announcement_id'])
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
