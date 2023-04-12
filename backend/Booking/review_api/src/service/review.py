from functools import lru_cache

from fastapi import Depends

from models.reviews import Review, Event
from db.models import base_classes
from db.mongo_storage import get_mongo
from db.redis_storage import get_redis

REDIS_INSTANCE = Depends(get_redis)
MONGO_INSTANCE = Depends(get_mongo)
RESULTS_COUNT = 100


class ReviewService:

    def __init__(self, redis: base_classes.Cache, mongo: base_classes.Storage):
        self.redis = redis
        self.mongo = mongo

    async def add_review(self, review: Review):
        await self.mongo.insert_document(review)

    async def update_review(self, review: Review):
        await self.mongo.update_document(review)

    async def get_document_by_id(self, review_id: str) -> Review:
        result = await self.redis.get_document_by_id(review_id)
        if not result:
            result = await self.mongo.get_document_by_id(review_id)
        else:
            return result
        if result:
            await self.redis.put_review_to_cache(result)
        return result

    async def get_all_reviews_for_event_id(self, event_id: str):
        reviews = await self.redis.get_document_by_event_id(event_id)
        if not reviews:
            reviews = await self.mongo.get_document_by_event_id(event_id)
        else:
            return reviews
        if reviews:
            await self.redis.put_reviews_to_cache(event_id, reviews)
        return reviews

    async def get_average_for_event_id(self, event_id: str) -> Event:
        return await self.mongo.get_average_by_event_id(event_id)


@lru_cache()
def get_review_service(
    redis: base_classes.Cache = REDIS_INSTANCE,
    mongo: base_classes.Storage = MONGO_INSTANCE,
) -> ReviewService:
    return ReviewService(redis=redis, mongo=mongo)