from datetime import datetime
from typing import TypedDict

from models.base import EventType
from models.context import context
from pydantic import BaseModel


class Event(BaseModel):
    notification_id: str
    source_name: str
    event_type: EventType
    context: context
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class EventConf(TypedDict):
    notification_id: str
    source_name: str
    event_type: EventType
    context: context
    created_at: datetime
