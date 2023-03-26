from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query

from api.v1.components.payload_announce import CreatePayload, UpdatePayload
from models.announcement import AnnouncementResponse, DetailAnnouncementResponse
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    '/announcement/{movie_id}',
    summary='Создание объявления',
    description='Создание записи в DB',
    response_model=DetailAnnouncementResponse,
    response_description='Подробная информация из объявления',
)
async def create(
    movie_id: str,
    payload: CreatePayload,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> DetailAnnouncementResponse:
    return HTTPStatus.OK


@router.put(
    '/announcement/{announcement_id}',
    summary='Изменение объявления',
    description='Изменение записи в DB',
    response_model=DetailAnnouncementResponse,
    response_description='Подробная информация после изменения',
)
async def update(
    announcement_id: str,
    payload: UpdatePayload,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> DetailAnnouncementResponse:
    return HTTPStatus.OK


@router.get(
    '/announcement/{announcement_id}',
    summary='Получить объявление по id',
    description='Получение всей информации по объявлению, сервис идет за информацией в db, UGC, Auth, Movie_api',
    response_model=DetailAnnouncementResponse,
    response_description='Подробная информация из объявления',
)
async def get_one(
    announcement_id: str,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> DetailAnnouncementResponse:
    return HTTPStatus.OK


@router.get(
    '/announcements',
    summary='Получить список всех объявлений',
    description='Получение списка объявлений, сервис идет за информацией в db',
    response_model=list[AnnouncementResponse],
    response_description='Список объявлений по условию',
)
async def get_multy(
    _author_filter: str | None = Query(default=None, alias='filter[author]'),
    _movie_filter: str | None = Query(default=None, alias='filter[movie]'),
    _free_filter: bool | None = Query(default=None, alias='filter[is_free]'),
    _sub_filter: bool | None = Query(default=None, alias='filter[private]'),
    _ticket_filter: int | None = Query(default=None, alias='filter[tickets]'),
    _date_filter: datetime | None = Query(default=None, alias='filter[date]'),
    _location_filter: str | None = Query(default=None, alias='filter[location]'),
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> list[AnnouncementResponse]:
    return HTTPStatus.OK


@router.delete(
    '/announcement/{announcement_id}',
    summary='Удаление объявления',
    description='Удаление записи из DB',
    response_description='HTTPStatus',
)
async def delete(
    announcement_id: str,
    # announcement_service: Any = '',  # noqa: E800
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> HTTPStatus:
    return HTTPStatus.OK
