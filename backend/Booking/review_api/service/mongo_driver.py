from motor import motor_asyncio


from models.reviews import Review
from core.config import settings


class MongoService:

    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(settings.mongo.uri)
        self.database = self.client[settings.mongo.DB]
        self.collection = self.database[self.collection]

    async def insert_document(self, _doc: Review):
        await self.collection.insert_one(_doc.json())
