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
