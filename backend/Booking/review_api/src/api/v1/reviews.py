import logging
import uuid
from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.config import settings
from src.models.announce import AnnouncementToReviewResponse
from src.models.noitifciations import NewReviewsLikes
from src.models.reviews import Event, Review, ReviewIncoming, UserReviewAvg
from src.service.booking import BookingService, get_booking_service
from src.service.review import ReviewService, get_review_service
from src.utils import auth
from src.utils.notific import NotificApiRepository, get_notific_repo

logger = logging.getLogger(__name__)
router = APIRouter()
auth_handler = auth.AuthHandler()
REVIEW_SERVICE_INSTANCE = Depends(get_review_service)
BOOKING_SERVICE_INSTANCE = Depends(get_booking_service)
NOTIFIC_SERVICE_INSTANCE = Depends(get_notific_repo)


@router.post(
    '/reviews/{announcement_id}',
    summary='Создание отзыва на событие',
    description='Создание отзыва',
    response_model=Review,
    response_description='Полное ревью события',
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    announcement_id: str,
    review: ReviewIncoming,
    _user: dict = Depends(auth_handler.auth_wrapper),
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
    booking_service: BookingService = BOOKING_SERVICE_INSTANCE,
    notific_service: NotificApiRepository = NOTIFIC_SERVICE_INSTANCE,
) -> Review:
    booking: AnnouncementToReviewResponse = await booking_service.get_booking(announcement_id, _user['user_id'])
    review = Review(
        **review.dict(),
        event_id=booking.announcement_id,
        guest_id=_user['user_id'],
        created=dt.utcnow(),
        modified=dt.utcnow(),
        id=uuid.uuid4(),
        author_id=booking.author_id,
    )
    await review_service.add_review(review)
    notification: NewReviewsLikes = NewReviewsLikes(
        author_name=booking.author_name,
        announce_title='New Review for booking',
        link=(
            f'http://{settings.review_api.HOST}:{settings.review_api.PORT}'
            f'/api/v1//reviews/{booking.announcement_id}/{review.id}'
        ),
        guest_name=_user.get('user_id'),
    )
    await notific_service.send(notification)
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
    '/average_score_for_event/{event_id}',
    summary='Получение среднего значения оценки по событию',
    description='Получение среднего значения оценки по событию',
    response_model=Event,
    response_description='Средняя оценка по событию',
)
async def get_average_for_event(
    event_id: str,
    _user: dict = Depends(auth_handler.auth_wrapper),
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
) -> Event:
    return await review_service.get_average_for_event_id(event_id)


@router.get(
    '/average_score/{user_id}',
    summary='Получение среднего значения оценки по событию',
    description='Получение среднего значения оценки по событию',
    response_model=UserReviewAvg,
    response_description='Средняя оценка по событию',
)
async def get_average(
    user_id: str,
    _user: dict = Depends(auth_handler.auth_wrapper),
    review_service: ReviewService = REVIEW_SERVICE_INSTANCE,
) -> Event:
    return await review_service.get_average_for_user(user_id)
