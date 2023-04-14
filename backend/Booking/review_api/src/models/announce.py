from uuid import UUID

from src.models.base import DefaultOrjsonModel


class AnnouncementToReviewResponse(DefaultOrjsonModel):
    author_id: str | UUID
    guest_id: str | UUID
    announcement_id: str | UUID
    author_name: str
    guest_name: str
    announcement_title: str
