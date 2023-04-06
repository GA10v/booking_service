from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from generator.src.models.base import EventType
from generator.src.models.context import NewContent, NewPromo, NewReviewsLikes


class Event(BaseModel):
    notification_id: UUID
    event_type: EventType
    context: NewContent | NewReviewsLikes | NewPromo
    created_at: datetime
    source_name: str

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
