from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from models.events import Event
from service.producer import RabbitMQProducerService, get_producer_service
from utils.fake_data import get_content_event, get_likes_event, get_promo_event, get_user_event

router = APIRouter()


@router.post(
    '/test_new_content',
    summary='Test new_content',
    description='Тест уведомления о новом контенте',
)
async def test_new_content(
    request: Request,
    payload: Event = Depends(get_content_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_likes',
    summary='Test new_likes',
    description='Тест уведомления о новых лайках на обзор',
)
async def test_new_likes(
    request: Request,
    payload: Event = Depends(get_likes_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_welcome',
    summary='Test welcome',
    description='Тест приветственного письма',
)
async def test_welcome(
    request: Request,
    payload: Event = Depends(get_user_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK


@router.post(
    '/test_promo',
    summary='Test new_promo',
    description='Тест кастомного уведомления',
)
async def test_promo(
    request: Request,
    payload: Event = Depends(get_promo_event),
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    await service.send_event(payload)
    return HTTPStatus.OK
