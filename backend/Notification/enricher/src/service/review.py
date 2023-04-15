from core.logger import get_logger
from db.storage import PGStorage
from models.events import Event

logger = get_logger(__name__)


async def update_storage(db: PGStorage, data: Event) -> None:
    logger.info('Update storage...')
