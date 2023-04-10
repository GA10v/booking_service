import logging
import json

from pydantic_collections import BaseCollectionModel
from redis import Redis

from db.models.base_classes import Cache
from models.reviews import Review
from core.config import settings


logger = logging.getLogger(__name__)


class ReviewCollection(BaseCollectionModel[Review]):
    pass


class RedisStorage(Cache):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def close(self):
        await self.redis.close()

    async def put_review_to_cache(self, review: Review):
        await self.redis.set(f'review::{review.id}', review.json(), ex=settings.redis.EXPIRE_SEC)

    async def get_document_by_id(self, review_id: str) -> Review:
        result = self.redis.get(f'review::{review_id}')
        if not result:
            return None
        return Review(json.loads(result))


redis: RedisStorage | None = None


async def get_redis() -> RedisStorage:
    return redis
