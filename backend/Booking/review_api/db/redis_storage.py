import logging

from pydantic_collections import BaseCollectionModel
from redis import Redis

from db.models.base_classes import Cache
from models.reviews import Review


logger = logging.getLogger(__name__)


class ReviewCollection(BaseCollectionModel[Review]):
    pass


class RedisStorage(Cache):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def close(self):
        await self.redis.close()


redis: RedisStorage | None = None


async def get_redis() -> RedisStorage:
    return redis
