from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventType(str, Enum):
    new_likes = 'new_likes'

    def __repr__(self) -> str:
        return f'{self.value}'


class NewReviewsLikes(BaseModel):
    author_id: str | UUID
    guest_id: str | UUID
    announcement_id: str | UUID


class NotificEvent(BaseModel):
    notification_id: str
    source_name: str
    event_type: EventType
    context: NewReviewsLikes
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
