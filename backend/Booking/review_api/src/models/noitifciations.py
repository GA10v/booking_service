from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    author_name: str
    announce_title: str
    link: str
    guest_name: str
