from functools import lru_cache

from fastapi import Depends

from models.reviews import Review, Event
from db.models import base_classes
from db.mongo_storage import get_mongo
from db.redis_storage import get_redis

from utils.notific import NotificApiRepository

REDIS_INSTANCE = Depends(get_redis)
MONGO_INSTANCE = Depends(get_mongo)
RESULTS_COUNT = 100


class ReviewService:

    def __init__(
            self,
            redis: base_classes.Cache,
            mongo: base_classes.Storage,
            notific: NotificApiRepository,
    ):
        self.redis = redis
        self.mongo = mongo
        self.notific = NotificApiRepository

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

    async def new_likes_create(
        self,
        guest_id: str | UUID,
        new_likes: None,  # TODO: add payload model
    ):
        """
        Запись новой оценки и оповещение хоста события.
        :param guest_id: id автора оценки
        :param new_likes: данные оценки
        """
        try:
            _guest = await self.notific.get_by_id(guest_id)  # TODO: нужен метод
            logger.info(f'Get guest with id {guest_id}: {_guest}>')
            _id = await self.notific.create(new_likes=new_likes, author_id=guest_id)  # TODO: нужен метод
            logger.info(f'[+] Create announcement <{_id}>')
        except exc.UniqueConstraintError:
            raise

        annouce = await self.get_one(_id)

        # оповещаем автора о новой оценке
        payload = NewScorePayload(announcement_id=_id, user_id=guest_id)
        await self.send(layer_payload.EventType.announce_new, payload)
        # TODO: поправить и продолжить

        return annouce


@lru_cache()
def get_review_service(
    redis: base_classes.Cache = REDIS_INSTANCE,
    mongo: base_classes.Storage = MONGO_INSTANCE,
) -> ReviewService:
    return ReviewService(redis=redis, mongo=mongo)
