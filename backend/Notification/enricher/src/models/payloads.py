from datetime import datetime
from typing import Union

from models.base import DeliveryType
from pydantic import BaseModel


class BaseUserContext(BaseModel):
    user_id: str
    user_name: str
    email: str
    phone_number: str | None
    telegram_name: str | None
    delivery_type: DeliveryType


class NewUserContext(BaseModel):
    user_name: str
    email: str
    link: str
    delivery_type: DeliveryType


class UserShortContext(BaseModel):
    user_id: str
    url: str
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class NewReviewsLikesContext(BaseUserContext):
    review_id: str
    movie_title: str
    likes: int


class NewContentContext(BaseUserContext):
    movie_title: str


class NewPromoContext(BaseUserContext):
    text_to_promo: str


payload = Union[NewUserContext, NewReviewsLikesContext, NewContentContext, NewPromoContext]
