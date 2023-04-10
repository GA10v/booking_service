import logging
import json

from redis import Redis

from db.models.base_classes import Cache
from models.reviews import Review, ReviewCollection
from core.config import settings


logger = logging.getLogger(__name__)


class RedisStorage(Cache):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def close(self):
        await self.redis.close()

    async def put_review_to_cache(self, review: Review):
        self.redis.set(f'review::{review.id}', review.json(), ex=settings.redis.EXPIRE_SEC)

    async def put_reviews_to_cache(self, event_id: str, reviews: ReviewCollection):
        self.redis.set(f'reviews::event_id::{event_id}', reviews, ex=settings.redis.EXPIRE_SEC)

    async def get_document_by_id(self, review_id: str) -> Review:
        result = self.redis.get(f'review::{review_id}')
        if not result:
            return None
        return Review.parse_obj(json.loads(result))

    async def get_document_by_event_id(self, event_id: str):
        result = self.redis.get(f'reviews::event_id::{event_id}')
        if not result:
            return None
        return ReviewCollection(json.loads(result))


redis: RedisStorage | None = None


async def get_redis() -> RedisStorage:
    return redis
