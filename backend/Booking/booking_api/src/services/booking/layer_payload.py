from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Role(str, Enum):
    guest = 'guest'
    author = 'author'


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


class PGCreatePayload(BaseModel):
    id: str | UUID
    announcement_id: str | UUID
    movie_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    event_time: datetime
