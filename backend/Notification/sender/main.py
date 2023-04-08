import asyncio
from typing import Any

from broker.consumer import RabbitMQConsumer
from models.notifications import TemplateToSender
from pydantic.error_wrappers import ValidationError
from v1.workers.generic_worker import Worker
from v1.workers.handler import get_worker

from core.logger import get_logger

logger = get_logger(__name__)

consumer = RabbitMQConsumer()


async def handler(message: dict[str, Any]) -> None:
    logger.info('Starting handler process...')
    try:
        notification = TemplateToSender(**message)
    except ValidationError as ex:
        logger.exception(f'Except {ex}')
        raise
    worker: Worker = await get_worker(data=notification)
    await worker().send_message(notification=notification)
    logger.info('Send')


async def sender() -> None:
    logger.info('Starting send process...')
    await consumer.consume(callback=handler)


if __name__ == '__main__':
    asyncio.run(sender())
