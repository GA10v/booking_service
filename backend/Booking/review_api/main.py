import logging
from contextlib import asynccontextmanager

import uvicorn
import redis
from fastapi import FastAPI
from motor import motor_asyncio

from src.api.v1 import reviews
from src.core.config import settings
from src.core.logger import LOGGING
from src.middleware.auth import auth_middleware
from src.middleware.logger import logging_middleware
from src.utils.sentry import init_sentry
from src.db import mongo_storage, redis_storage

init_sentry()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_instance = redis.from_url(
        settings.redis.uri,
        decode_responses=True,
    )
    redis_storage.redis = redis_storage.RedisStorage(redis_instance)
    mongo_instance = motor_asyncio.AsyncIOMotorClient(settings.mongo.uri)
    mongo_storage.mongo = mongo_storage.MongoStorage(mongo_instance)
    yield
    await redis_storage.redis.close()
    mongo_storage.mongo = None  # autoclose in 5 minutes default

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
)

# middleware
logging_middleware(app=app)
if not settings.debug.DEBUG:
    auth_middleware(app=app)

# @app.on_event('startup')
# async def startup():
#     await init_models()
#     # TODO: инициализация брокеров, очередей (если 1-й вариант в работе)


# @app.on_event('shutdown')
# async def shutdown():
#     ...
#     # TODO: закрыть все, выключить свет


app.include_router(reviews.router, prefix=settings.review_api.API_PREFIX, tags=['reviews'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=settings.review_api.PORT, log_config=LOGGING, log_level=logging.DEBUG)
