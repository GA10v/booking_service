from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    review_id: str
    author_id: str
    movie_id: str
    likes: int
