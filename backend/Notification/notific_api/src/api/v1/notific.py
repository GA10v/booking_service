from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from models.events import Event, EventConf
from pydantic.error_wrappers import ValidationError
from service.producer import RabbitMQProducerService, get_producer_service

router = APIRouter()


@router.post(
    '/send',
    summary='Notification',
    description='Отправка уведомления в очередь RebbitMQ',
)
async def send_notific(
    request: Request,
    payload: EventConf,
    service: RabbitMQProducerService = Depends(get_producer_service),
) -> HTTPStatus:

    try:
        _payload = Event(**payload)
    except ValidationError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Wrong entry')

    await service.send_event(_payload)
    return HTTPStatus.OK
