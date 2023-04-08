import json
from abc import ABC, abstractmethod

import aio_pika
from aio_pika import DeliveryMode, ExchangeType, Message

from core.config import settings


class ProducerProtocol(ABC):
    @abstractmethod
    async def init_producer(
        self,
        uri: str,
        incoming_queue: str,
        retry_queue: str,
        incoming_exchange: str,
        retry_exchange: str,
        **kwargs,
    ) -> None:
        ...

    @abstractmethod
    async def send_msg(self, msg: dict, **kwargs) -> None:
        ...


class RabbitMQProducer(ProducerProtocol):
    def __init__(self) -> None:
        self.connection = None
        self.channel = None
        self.incoming_queue_to_enrich = None
        self.retry_queue_to_enrich = None
        self.incoming_exchange_to_enrich = None
        self.retry_exchange_to_enrich = None
        self.incoming_queue_to_send = None
        self.retry_queue_to_send = None
        self.incoming_exchange_to_send = None
        self.retry_exchange_to_send = None

    async def init_producer(
        self,
        uri: str,
        incoming_queue_to_enrich: str,
        retry_queue_to_enrich: str,
        incoming_exchange_to_enrich: str,
        retry_exchange_to_enrich: str,
        incoming_queue_to_send: str,
        retry_queue_to_send: str,
        incoming_exchange_to_send: str,
        retry_exchange_to_send: str,
        **kwargs,
    ) -> None:
        self.connection = await aio_pika.connect_robust(uri)
        self.channel = await self.connection.channel()
        self.incoming_queue_to_enrich = await self.channel.declare_queue(
            name=incoming_queue_to_enrich,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_RETRY_1.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        self.retry_queue_to_enrich = await self.channel.declare_queue(
            name=retry_queue_to_enrich,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_INCOMING_1.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        self.incoming_exchange_to_enrich = await self.channel.declare_exchange(
            name=incoming_exchange_to_enrich,
            type=ExchangeType.DIRECT,
            durable=True,
        )
        self.retry_exchange_to_enrich = await self.channel.declare_exchange(
            name=retry_exchange_to_enrich,
            type=ExchangeType.FANOUT,
            durable=True,
        )
        self.incoming_queue_to_send = await self.channel.declare_queue(
            name=incoming_queue_to_send,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_RETRY_2.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        self.retry_queue_to_send = await self.channel.declare_queue(
            name=retry_queue_to_send,
            durable=True,
            arguments={
                'x-dead-letter-exchange': settings.rabbit.EXCHENGE_INCOMING_2.lower(),
                'x-message-ttl': settings.rabbit.MESSAGE_TTL_MS,
            },
        )
        self.incoming_exchange_to_send = await self.channel.declare_exchange(
            name=incoming_exchange_to_send,
            type=ExchangeType.DIRECT,
            durable=True,
        )
        self.retry_exchange_to_send = await self.channel.declare_exchange(
            name=retry_exchange_to_send,
            type=ExchangeType.FANOUT,
            durable=True,
        )
        await self.incoming_queue_to_enrich.bind(self.incoming_exchange_to_enrich)
        await self.retry_queue_to_enrich.bind(self.retry_exchange_to_enrich)
        await self.incoming_queue_to_send.bind(self.incoming_exchange_to_send)
        await self.retry_queue_to_send.bind(self.retry_exchange_to_send)

    async def send_msg(self, msg: dict, **kwargs) -> None:
        message = Message(
            body=json.dumps(msg).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
            headers={},
        )
        await self.incoming_exchange_to_enrich.publish(
            message=message,
            routing_key=self.incoming_queue_to_enrich.name,
        )


producer: RabbitMQProducer = RabbitMQProducer()


async def get_producer() -> RabbitMQProducer:
    return producer
