from uuid import UUID

from core.logger import get_logger
from services.announcement import layer_models
from services.announcement.repositories import _protocols, rating_repo, user_repo

logger = get_logger(__name__)


class BookingMockRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        logger.info('BookingMockRepository init ...')

    async def _fake_boking(self) -> layer_models.BookingToDetailResponse:
        return layer_models.BookingToDetailResponse(
            guest_name=await self.user_repo.get_by_id('fake_uuid'),
            guest_rating=await self.rating_repo.get_by_id('fake_uuid'),
            guest_status=True,
        )

    async def get_by_id(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        return [await self._fake_boking() for _ in 5]


class BookingSqlachemyRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self) -> None:
        self.user_repo = user_repo.get_user_repo()
        self.rating_repo = rating_repo.get_rating_repo()
        logger.info('BookingSqlachemyRepository init ...')
        ...


def get_booking_repo() -> _protocols.BookingRepositoryProtocol:
    return BookingMockRepository
