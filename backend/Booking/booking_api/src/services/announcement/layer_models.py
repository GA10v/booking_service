from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class BookingToDetailResponse(BaseModel):
    guest_name: str
    guest_rating: float
    guest_status: bool


class EventStatus(str, Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class AnnouncementResponse(BaseModel):
    announcement_id: str | UUID
    status: EventStatus
    title: str
    author_id: str | UUID
    sub_only: bool
    is_free: bool
    ticket_count: int
    event_time: datetime
    event_location: str

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['announcement_id'] = str(_dict['announcement_id'])
        _dict['author_id'] = str(_dict['author_id'])
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


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
    event_time: datetime
    event_location: str
    guest_list: list[str]
    author_rating: float

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['id'] = str(_dict['id'])
        _dict['created'] = _dict['created'].strftime('%Y-%m-%d %H:%M:%S')
        _dict['modified'] = _dict['modified'].strftime('%Y-%m-%d %H:%M:%S')
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
