from datetime import datetime

from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    author_name: str
    announce_title: str
    link: str
    guest_name: str


class NotificEvent(BaseModel):
    notification_id: str
    source_name: str
    event_type: str
    context: NewReviewsLikes
    created_at: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['created_at'] = _dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
