
from motor import AsyncIOMotorClient

from db.models.base_classes import Storage
from models.reviews import Review
from core.config import settings


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
        return self.collection.find(filter={'event_id': event_id})

    async def get_document_by_id(self, review_id: str) -> Review:
        return Review.from_obj(self.collection.find_one(filter={'id': review_id}))


mongo: MongoStorage | None = None


async def get_mongo() -> MongoStorage:
    return mongo
