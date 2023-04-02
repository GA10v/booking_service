from datetime import datetime

from pydantic import BaseModel


class UpdatePayload(BaseModel):
    my_status: bool


class MultyPayload(BaseModel):
    is_self: bool | None
    author: str | None
    movie: str | None
    date: datetime | None
