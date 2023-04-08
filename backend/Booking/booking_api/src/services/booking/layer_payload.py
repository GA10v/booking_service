from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Role(str, Enum):
    guest = 'guest'
    author = 'author'

    def __repr__(self) -> str:
        return f'{self.value}'


class APIUpdatePayload(BaseModel):
    my_status: bool


class SudoAPIMultyPayload(BaseModel):
    is_self: bool | None
    author: str | None
    movie: str | None
    date: datetime | None


class APIMultyPayload(BaseModel):
    role: Role
    movie: str | None
    date: datetime | None


class EventStatus(str, Enum):
    Created = 'Created'
    Alive = 'Alive'
    Closed = 'Closed'
    Done = 'Done'

    def __repr__(self) -> str:
        return f'{self.value}'


class AnnounceToCreate(BaseModel):
    status: EventStatus
    announce_id: str | UUID
    author_id: str | UUID
    movie_id: str | UUID
    event_time: datetime


class PGCreatePayload(BaseModel):
    id: str | UUID
    announcement_id: str | UUID
    movie_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    event_time: datetime
