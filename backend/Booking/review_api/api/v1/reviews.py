import logging
import uuid
from datetime import datetime as dt

from fastapi import APIRouter, Depends, status, HTTPException

from models.reviews import Review, ReviewIncoming, Event
from service.review import ReviewService, get_review_service
from service.booking import BookingService, get_booking_service
from utils import auth


logger = logging.getLogger(__name__)
router = APIRouter()
auth_handler = auth.AuthHandler()
REVIEW_SERVICE_INSTANCE = Depends(get_review_service)
BOOKING_SERVCIE_INSTANCE = Depends(get_booking_service)


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
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
    booking_service: BookingService = BOOKING_SERVCIE_INSTANCE,
) -> Review:
    booking = await booking_service.get_booking(event_id)
    review = Review(
        **review.dict(),
        event_id=event_id,
        guest_id=_user['user_id'],
        created=dt.utcnow(),
        modified=dt.utcnow(),
        id=uuid.uuid4(),
    )
    await review_service.add_review(review)
    logger.info(f'And sending to: {booking.author_id}')
    return review


@router.put(
    '/reviews/{event_id}/{review_id}',
    summary='Изменение отзыва на событие',
    description='Изменение отзыва',
    response_model=Review,
    response_description='Обновлённое ревью события',
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_review(
    event_id: str,
    review_id: str,
    review: ReviewIncoming,
    _user: dict = Depends(auth_handler.auth_wrapper),
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
) -> Review:
    review_db: Review = await review_service.get_document_by_id(review_id)
    if not review_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if event_id != review_db.event_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Review is not attibuted to Event.')
    if review_db.guest_id != _user['user_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not your review.')
    review = Review(
        **review.dict(),
        event_id=event_id,
        guest_id=_user['user_id'],
        modified=dt.utcnow(),
        created=review_db.created,
        id=review_db.id,
    )
    await review_service.update_review(review)
    return review


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
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
) -> Review:
    review_db: Review = await review_service.get_document_by_id(review_id)
    if review_db.event_id != event_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return review_db


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
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
) -> list[Review]:
    return await review_service.get_all_reviews_for_event_id(event_id)


@router.get(
    '/average_score/{event_id}',
    summary='Получение среднего значения оценки по событию',
    description='Получение среднего значения оценки по событию',
    response_model=Event,
    response_description='Средняя оценка по событию',
)
async def get_average(
    event_id: str,
    _user: dict = Depends(auth_handler.auth_wrapper),
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
) -> Event:
    return await review_service.get_average_for_event_id(event_id)
