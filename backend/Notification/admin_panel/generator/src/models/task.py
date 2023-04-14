from generator.src.models.base import EventType
from pydantic import BaseModel


class Task(BaseModel):
    event_type: EventType
    movie_id: str | None
    group_id: str | None
    text_to_promo: str | None
