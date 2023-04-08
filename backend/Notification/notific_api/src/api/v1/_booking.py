from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from models.events import Event
from service.producer import RabbitMQProducerService, get_producer_service
from utils import fake_data

router = APIRouter()


@router.post(
    '/test_delete_booking',
    summary='Test delete_booking',
    description='Тест уведомления после удаления заявки',
)
async def test_delete_booking(
    request: Request,
    payload: Event = Depends(fake_data.get_delete_booking_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_new_booking',
    summary='Test new_booking',
    description='Тест уведомления после создания заявки',
)
async def test_new_booking(
    request: Request,
    payload: Event = Depends(fake_data.get_new_booking_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_status_booking',
    summary='Test status_booking',
    description='Тест уведомления после изменения заявки',
)
async def test_status_booking(
    request: Request,
    payload: Event = Depends(fake_data.get_status_booking_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK
