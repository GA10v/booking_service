import logging
import uuid
from datetime import datetime as dt

from fastapi import APIRouter, Depends, status

from models.reviews import Review, ReviewIncoming
from service.mongo_driver import MongoService
from utils import auth


logger = logging.getLogger(__name__)
router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    '/reviews/{event_id}',
    summary='Создание отзыва на событие',
    description='Создание отзыва',
    response_model=Review,
    response_description='Полное ревью события',
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    event_id: str,
    review: ReviewIncoming,
    _user: dict = Depends(auth_handler.auth_wrapper),
    mongo_service: MongoService = Depends(),
) -> Review:
    review = Review(
        **review.dict(),
        event_id=event_id,
        guest_id=_user['user_id'],
        created=dt.utcnow(),
        modified=dt.utcnow(),
        id=uuid.uuid4(),
    )
    logger.info(review)
    await mongo_service.insert_document(review)
    return review


@router.put(
    '/reviews/{event_id}/{review_id}',
    summary='Изменение отзыва на событие',
    description='Изменение отзыва',
    response_model=Review,
    response_description='Обновлённое ревью события',
)
async def update_review(
    event_id: str,
    review_id: str,
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> Review:
    # review = Review(**review.dict(), event_id=event_id, guest_id=_user['sub'])
    return status.HTTP_200_OK


@router.get(
    '/reviews/{event_id}/{review_id}',
    summary='Получение отзыва на событие',
    description='Получение отзыва',
    response_model=Review,
    response_description='Ревью события',
)
async def get_review(
    event_id: str,
    review_id: str,
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> Review:
    return status.HTTP_200_OK


@router.get(
    '/reviews/{event_id}',
    summary='Получение всех отзывов на событие',
    description='Получение всех отзывов',
    response_model=list[Review],
    response_description='Список ревью события',
)
async def get_reviews(
    event_id: str,
    _user: dict = Depends(auth_handler.auth_wrapper),
    mongo_service: MongoService = Depends(),
) -> Review:
    results = mongo_service.get_document_by_event_id(event_id)
    logger.info(results)
    return results
