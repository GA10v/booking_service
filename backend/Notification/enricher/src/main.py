import asyncio
from typing import Any

from broker.consumer import RabbitMQConsumer
from broker.producer import RabbitMQProducer
from db.storage import PGStorage
from models.events import Event
from pydantic.error_wrappers import ValidationError
from service.builder import BuilderService
from service.enrich.handler import get_payload
from service.review import update_storage
from service.template import get_template

from core.logger import get_logger

logger = get_logger(__name__)

consumer = RabbitMQConsumer()
producer = RabbitMQProducer()
enricher = BuilderService()
db = PGStorage()


async def handler(message: dict[str, Any]) -> None:
    try:
        event = Event(**message)
    except ValidationError as ex:
        logger.exception(f'Except {ex}')
        raise
    async with db as conn:
        _template = await get_template(db=conn, data=event)
    payload = await get_payload(data=event)
    new_message = await enricher.build(
        data=payload,
        template=_template,
        notification_id=event.notification_id,
    )
    await producer.publish(msg=new_message)
    async with db as conn:
        await update_storage(db=conn, data=event)
        logger.info('Starting enricher process...')


async def builder() -> None:
    logger.info('Starting enricher process...')
    await consumer.consume(callback=handler)


if __name__ == '__main__':
    asyncio.run(builder())
