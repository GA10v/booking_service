import enum
from datetime import datetime

from pydantic import BaseModel


class EventStatus(str, enum.Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class CreatePayload(BaseModel):
    status: EventStatus
    title: str
    description: str
    sub_only: bool
    is_free: bool
    tickets_count: int
    event_time: datetime
    event_location: str


class UpdatePayload(BaseModel):
    status: EventStatus | None
    movie_id: str | None
    title: str | None
    description: str | None
    sub_only: bool | None
    is_free: bool | None
    tickets_count: int | None
    event_time: datetime | None
    event_location: str | None
