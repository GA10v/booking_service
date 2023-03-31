import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventStatus(str, enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


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

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['id'] = str(_dict['id'])
        _dict['movie_id'] = str(_dict['movie_id'])
        _dict['author_id'] = str(_dict['author_id'])
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


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
    author_filter: str | None
    movie_filter: str | None
    is_free_filter: bool | None
    sub_filter: bool | None
    ticket_filter: int | None
    date_filter: datetime | None
    location_filter: str | None
