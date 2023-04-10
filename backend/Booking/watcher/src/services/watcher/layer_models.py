from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class UpdateStatus(BaseModel):
    announcement_id: str | UUID
    status: bool


class EventStatus(str, Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class BookingToDetailResponse(BaseModel):
    booking_id: str | UUID
    guest_id: str | UUID
    guest_name: str
    guest_rating: float
    guest_status: bool
    author_status: bool | None


class DetailAnnouncementResponse(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
    status: EventStatus
    title: str
    description: str
    movie_title: str
    author_name: str
    sub_only: bool
    is_free: bool
    tickets_count: int
    tickets_left: int
    event_time: datetime
    event_location: str
    guest_list: list[BookingToDetailResponse]
    author_rating: float
    duration: int
