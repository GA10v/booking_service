from functools import lru_cache

from fastapi import Depends

from models.reviews import Review
from db.models import base_classes
from db.mongo_storage import get_mongo
from db.redis_storage import get_redis

REDIS_INSTANCE = Depends(get_redis)
MONGO_INSTANCE = Depends(get_mongo)


class ReviewService:

    def __init__(self, redis: base_classes.Cache, mongo: base_classes.Storage):
        self.redis = redis
        self.mongo = mongo

    async def add_review(self, review: Review):
        await self.mongo.insert_document(review)

    async def update_review(self, review: Review):
        await self.mongo.update_document(review)

    async def get_document_by_id(self, review_id: str) -> Review:
        return await self.mongo.find_one(review_id)

    async def get_all_reviews_for_event_id(self, event_id: str):
        reviews = await self.mongo.get_document_by_event_id(event_id)
        return [Review.parse_obj(review) async for review in reviews]


@lru_cache()
def get_review_service(
    redis: base_classes.Cache = REDIS_INSTANCE,
    mongo: base_classes.Storage = MONGO_INSTANCE,
) -> ReviewService:
    return ReviewService(redis=redis, mongo=mongo)
