"""Models to describe review."""
from enum import Enum
from uuid import UUID

from pydantic_collections import BaseCollectionModel

from src.models.base import DefaultModel, DefaultOrjsonModel


class ReviewBase(DefaultModel):
    """Class with common options to all models."""

    guest_id: str | UUID
    event_id: str | UUID

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['guest_id'] = str(_dict['guest_id'])
        _dict['event_id'] = str(_dict['event_id'])
        return _dict


class Review(ReviewBase):
    """Class to describe Review instance."""

    review_text: str
    score: int


class ReviewIncoming(DefaultOrjsonModel):
    """Class to collect data from guest."""

    review_text: str
    score: int


class Event(DefaultOrjsonModel):

    event_id: str
    score_average: float


class UserReviewAvg(DefaultOrjsonModel):

    score_average: float


class ReviewCollection(BaseCollectionModel[Review]):
    pass


class EventType(str, Enum):
    new_content = 'new_content'
    new_likes = 'new_likes'
    promo = 'promo'
    score_request = 'score_request'

    def __repr__(self) -> str:
        return f'{self.value}'
