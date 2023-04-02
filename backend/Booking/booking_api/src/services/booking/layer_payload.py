from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class APIUpdatePayload(BaseModel):
    my_status: bool


class APIMultyPayload(BaseModel):
    is_self: bool | None
    author: str | None
    movie: str | None
    date: datetime | None


class PGCreatePayload(BaseModel):
    id: str | UUID
    announcement_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    event_time: datetime
