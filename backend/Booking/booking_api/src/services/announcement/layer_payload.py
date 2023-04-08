import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventStatus(str, enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'


class APICreatePayload(BaseModel):
    status: EventStatus
    title: str
    description: str
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str


class PGCreatePayload(BaseModel):
    id: str | UUID
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


class APIUpdatePayload(BaseModel):
    status: EventStatus | None
    title: str | None
    description: str | None
    sub_only: bool | None
    is_free: bool | None
    tickets_count: int | None
    event_time: datetime | None
    event_location: str | None


class APIMultyPayload(BaseModel):
    author: str | None
    movie: str | None
    free: bool | None
    sub: bool | None
    ticket: int | None
    date: datetime | None
    location: str | None
