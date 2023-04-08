from datetime import datetime

from models.base import DeliveryType
from pydantic import BaseModel


class TemplateFromDB(BaseModel):
    subject: str
    template_files: str
    text_msg: str


class ReviewsFromDB(BaseModel):
    pkid: str
    movie_id: str
    author_id: str
    review_id: str
    likes_count: int
    modified: datetime


class TemplateToSender(BaseModel):
    notification_id: str
    user_id: str | None
    subject: str
    email_body: str
    ws_body: str | None
    recipient: list[str]
    delivery_type: DeliveryType
