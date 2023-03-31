import random
from uuid import UUID

from core.logger import get_logger
from services.announcement.repositories import _protocols

logger = get_logger(__name__)


class RatingMockRepository(_protocols.RatingRepositoryProtocol):
    def __init__(self) -> None:
        logger.info('RatingMockRepository init ...')

    async def get_by_id(self, user_id: str | UUID) -> float:
        return random.uniform(0.0, 10.0)


def get_rating_repo() -> _protocols.RatingRepositoryProtocol:
    return RatingMockRepository()
