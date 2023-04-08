from pydantic import BaseModel

from generator.src.models.base import EventType


class Task(BaseModel):
    event_type: EventType
    movie_id: str | None
    group_id: str | None
    text_to_promo: str | None
