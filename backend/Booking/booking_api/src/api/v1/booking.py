from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query

from api.v1.components.payload_booking import UpdatePayload
from models.booking import BookingResponse, DetailBookingResponse
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    '/booking/{announcement_id}',
    summary='Создание заявки',
    description='Создание записи в DB',
    response_model=DetailBookingResponse,
    response_description='Подробная информация из заявки',
)
async def create(
    announcement_id: str,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> DetailBookingResponse:
    return HTTPStatus.OK


@router.put(
    '/booking/{booking_id}',
    summary='Изменение статуса заявки',
    description='Изменение записи в DB',
    response_model=DetailBookingResponse,
    response_description='Подробная информация после изменения',
)
async def update(
    announcement_id: str,
    payload: UpdatePayload,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> DetailBookingResponse:
    return HTTPStatus.OK


@router.get(
    '/booking/{booking_id}',
    summary='Получить заявки по id',
    description='Получение всей информации по заявке, сервис идет за информацией в db, Auth, Movie_api',
    response_model=DetailBookingResponse,
    response_description='Подробная информация из объявления',
)
async def get_one(
    booking_id: str,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> DetailBookingResponse:
    return HTTPStatus.OK


@router.get(
    '/bookings',
    summary='Получить список всех объявлений',
    description='Получение списка объявлений, сервис идет за информацией в db',
    response_model=list[BookingResponse],
    response_description='Список объявлений по условию',
)
async def get_multy(
    _announcement_filter: datetime | None = Query(default=None, alias='filter[announcement]'),
    _self_filter: bool | None = Query(default=None, alias='filter[self]'),
    _movie_filter: str | None = Query(default=None, alias='filter[movie]'),
    _date_filter: datetime | None = Query(default=None, alias='filter[date]'),
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> list[BookingResponse]:
    return HTTPStatus.OK


@router.delete(
    '/booking/{booking_id}',
    summary='Удаление заявки',
    description='Удаление записи из DB',
    response_description='HTTPStatus',
)
async def delete(
    booking_id: str,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> HTTPStatus:
    return HTTPStatus.OK
