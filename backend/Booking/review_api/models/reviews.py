"""Models to describe review."""

from models.base import DefaultModel, DefaultOrjsonModel
from uuid import UUID

from pydantic_collections import BaseCollectionModel


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


class ReviewCollection(BaseCollectionModel[Review]):
    pass
