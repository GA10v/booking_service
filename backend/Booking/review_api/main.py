import logging

import uvicorn
from fastapi import FastAPI

from api.v1 import reviews
from core.config import settings
from core.logger import LOGGING
from middleware.auth import auth_middleware
from middleware.logger import logging_middleware
from utils.sentry import init_sentry

init_sentry()

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
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


app.include_router(reviews.router, prefix=settings.fastapi.API_PREFIX, tags=['reviews'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8081, log_config=LOGGING, log_level=logging.DEBUG)