from uuid import UUID

from pydantic import BaseModel


class NewReviewsLikes(BaseModel):
    # the same names as in DB
    review_id: UUID
    author_id: UUID
    movie_id: UUID
    likes_count: int

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['review_id'] = str(_dict['review_id'])
        _dict['author_id'] = str(_dict['author_id'])
        _dict['movie_id'] = str(_dict['movie_id'])
        return _dict


class NewContent(BaseModel):
    user_id: UUID
    movie_id: str

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['user_id'] = str(_dict['user_id'])
        return _dict


class NewPromo(BaseModel):
    user_id: UUID
    text_to_promo: str

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['user_id'] = str(_dict['user_id'])
        return _dict
