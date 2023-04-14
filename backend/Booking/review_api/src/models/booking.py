from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class PGBooking(BaseModel):
    id: str | UUID
    created: datetime
    modified: datetime
    announcement_id: str | UUID
    movie_id: str | UUID
    author_id: str | UUID
    guest_id: str | UUID
    author_status: bool | None
    guest_status: bool | None
    event_time: datetime
