from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventStatus(Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'


class PGAnnouncement(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
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
    duration: int


class DoneAnnounce(BaseModel):
    done_announce_id: str | UUID
    user_id: str | UUID


class EventType(str, Enum):
    announce_done = 'announce_done'

    def __repr__(self) -> str:
        return f'{self.value}'


class NotificEvent(BaseModel):
    notification_id: str
    source_name: str
    event_type: EventType
    context: DoneAnnounce
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
