import json
from abc import ABC, abstractmethod
from typing import Any

from aio_pika import DeliveryMode, ExchangeType, Message
from broker.rabbit import RabbitMQBroker

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class ProducerProtocol(ABC):
    @abstractmethod
    async def publish(self, msg: dict[str, Any], **kwargs) -> None:
        ...


class RabbitMQProducer(ProducerProtocol, RabbitMQBroker):
    def __init__(
        self,
        incoming_queue: str = settings.rabbit.QUEUE_TO_SEND.lower(),
        retry_queue: str = settings.rabbit.QUEUE_RETRY_SEND.lower(),
        incoming_exchange: str = settings.rabbit.EXCHENGE_INCOMING_2.lower(),
        retry_exchange: str = settings.rabbit.EXCHENGE_RETRY_2.lower(),
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.incoming_queue = incoming_queue
        self.retry_queue = retry_queue
        self.incoming_exchange = incoming_exchange
        self.retry_exchange = retry_exchange

    async def publish(self, msg: dict[str, Any], **kwargs) -> None:
        if not self.channel_pool:
            await self.get_channel_pool()

        async with self.channel_pool.acquire() as channel:
            incoming_exchange = await channel.declare_exchange(
                name=self.incoming_exchange,
                type=ExchangeType.DIRECT,
                durable=True,
            )
            retry_exchange = await channel.declare_exchange(
                name=self.retry_exchange,
                type=ExchangeType.FANOUT,
                durable=True,
            )
            incoming_queue = await channel.declare_queue(
                name=self.incoming_queue,
                durable=True,
                auto_delete=False,
                arguments={
                    'x-dead-letter-exchange': self.retry_exchange,
                    'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
                },
            )
            retry_queue = await channel.declare_queue(
                name=self.retry_queue,
                durable=True,
                arguments={
                    'x-dead-letter-exchange': self.incoming_exchange,
                    'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
                },
            )

            await incoming_queue.bind(incoming_exchange)
            await retry_queue.bind(retry_exchange)

            message = Message(
                body=json.dumps(msg).encode('utf-8'),
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await incoming_exchange.publish(
                message=message,
                routing_key=self.incoming_queue,
            )
            logger.info(f'Message publish to<{self.incoming_queue}> : body<{msg}>')
