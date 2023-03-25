import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.base import DefaultModel


class EventStatus(str, enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class PGAnnouncement(DefaultModel):
    status: EventStatus
    title: str
    description: str
    movie_id: str | UUID
    author_id: str | UUID
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['movie_id'] = str(_dict['movie_id'])
        _dict['author_id'] = str(_dict['author_id'])
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class AnnouncementResponse(BaseModel):
    id: str | UUID
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
        _dict['id'] = str(_dict['id'])
        _dict['author_id'] = str(_dict['author_id'])
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class DetailAnnouncementResponse(PGAnnouncement):
    guest_list: list[str]
    rating: float
