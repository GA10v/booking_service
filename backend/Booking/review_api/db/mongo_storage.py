import logging

from motor.motor_asyncio import AsyncIOMotorClient

from db.models.base_classes import Storage
from models.reviews import Review, Event, ReviewCollection
from core.config import settings


logger = logging.getLogger(__name__)


class MongoStorage(Storage):

    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.database = self.client[settings.mongo.DB]
        self.collection = self.database[settings.mongo.REVIEW_COLLECTION]

    async def close(self):
        pass

    async def insert_document(self, _doc: Review):
        await self.collection.insert_one(_doc.dict())

    async def get_document_by_event_id(self, event_id: str) -> Review:
        result_generator = self.collection.find(filter={'event_id': event_id})
        reviews = [Review.parse_obj(review) async for review in result_generator]
        return ReviewCollection(reviews)

    async def get_document_by_id(self, review_id: str) -> Review:
        return Review.parse_obj(await self.collection.find_one(filter={'id': review_id}))

    async def update_document(self, _doc: Review):
        await self.collection.update_one(
            {'id': _doc.id},
            {'$set': {
                'review_text': _doc.review_text,
                'score': _doc.score,
                'modified': _doc.modified,
            }})

    async def get_average_by_event_id(self, event_id: str):
        pipeline = [{'$group': {'_id': event_id, 'score_average': {'$avg': '$score'}}}]
        doc = await self.collection.aggregate(pipeline).next()
        doc['event_id'] = doc.pop('_id')
        return Event.parse_obj(doc)


mongo: MongoStorage | None = None


async def get_mongo() -> MongoStorage:
    return mongo
