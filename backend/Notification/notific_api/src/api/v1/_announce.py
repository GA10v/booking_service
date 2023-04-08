from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from models.events import Event
from service.producer import RabbitMQProducerService, get_producer_service
from utils import fake_data

router = APIRouter()


@router.post(
    '/test_new_announce',
    summary='Test new_announce',
    description='Тест уведомления о создании объявления',
)
async def test_new_announce(
    request: Request,
    payload: Event = Depends(fake_data.get_new_announce_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_put_announce',
    summary='Test put_announce',
    description='Тест уведомления об изменении объявления',
)
async def test_put_announce(
    request: Request,
    payload: Event = Depends(fake_data.get_put_announce_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_delete_announce',
    summary='Test delete_announce',
    description='Тест уведомления об удалении объявления',
)
async def test_delete_announce(
    request: Request,
    payload: Event = Depends(fake_data.get_delete_announce_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_done_announce',
    summary='Test done_announce',
    description='Тест уведомления завершении события',
)
async def test_done_announce(
    request: Request,
    payload: Event = Depends(fake_data.get_done_announce_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK
