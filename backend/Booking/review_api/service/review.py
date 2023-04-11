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


from datetime import datetime
from functools import lru_cache
from uuid import uuid4

import aiohttp

from core.config import settings
from core.logger import get_logger
from db.redis import get_cache
from services.announcement import layer_payload
from services.announcement.repositories import _protocols
from utils.auth import _headers

logger = get_logger(__name__)


class NotificApi(_protocols.NotificRepositoryProtocol):
    def __init__(self) -> None:
        self.notific_endpoint = f'{settings.notific.uri}send'
        self._headers = _headers()
        self.redis = get_cache()

        logger.info('NotificApi init ...')

    async def send(self, event_type: layer_payload.EventType , payload: layer_payload.context) -> None:
        event = layer_payload.NotificEvent(
            notification_id=str(uuid4()),
            source_name='Review service',
            event_type=event_type,
            context=payload.dict(),
            created_at=datetime.now(),
        ).dict()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.notific_endpoint,
                headers=self._headers,
                json=event,
            ) as resp:
                logger.info(f'Send notific <{self.notific_endpoint}>')
                logger.info(f'Send notific resp.status: <{resp.status}>')


@lru_cache()
def get_notific_repo() -> _protocols.NotificRepositoryProtocol:
    return NotificApi()
