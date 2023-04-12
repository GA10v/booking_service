import enum
from datetime import datetime

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

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
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

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        if _dict['event_time']:
            _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class APIMultyPayload(BaseModel):
    author: str | None
    movie: str | None
    free: bool | None
    sub: bool | None
    ticket: int | None
    date: datetime | None
    location: str | None

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        if _dict['event_time']:
            _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


create_payload = APICreatePayload(
    status=EventStatus.Created.value,
    title='Fake Title',
    description='Fake description',
    sub_only=False,
    is_free=True,
    tickets_count=2,
    event_time=datetime.now(),
    event_location='Fake location',
).dict()

update_payload = APIUpdatePayload(
    status=EventStatus.Alive.value,
    title=None,
    description=None,
    sub_only=None,
    is_free=None,
    tickets_count=None,
    event_time=None,
    event_location=None,
).dict()
