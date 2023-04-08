from datetime import datetime

from models.base import EventType
from models.context import context
from pydantic import BaseModel


class Event(BaseModel):
    notification_id: str
    source_name: str
    event_type: EventType
    context: context
    created_at: datetime
