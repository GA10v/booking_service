import logging

import uvicorn
from api.v1 import test
from core.config import settings
from core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    ...
    # TODO: инициализация BD
    # TODO: инициализация брокеров, очередей (если 1-й вариант в работе)


@app.on_event('shutdown')
async def shutdown():
    ...
    # TODO: закрыть все, выключить свет


app.include_router(test.router, prefix=settings.fastapi.API_PREFIX, tags=['test'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, log_config=LOGGING, log_level=logging.DEBUG)
