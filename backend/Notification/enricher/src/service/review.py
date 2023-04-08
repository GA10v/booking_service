from datetime import datetime
from uuid import uuid4

from db.models.review_info import ReviewInfo
from db.storage import PGStorage
from models.base import EventType
from models.events import Event
from sqlalchemy import insert, select, update

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


async def update_storage(db: PGStorage, data: Event) -> None:
    logger.info('Update storage...')

    if data.event_type == EventType.new_likes:
        if settings.debug:
            query = select(ReviewInfo.review_id).filter(ReviewInfo.review_id == data.context.review_id)
            _res = await db.execute(query)
            if not _res:
                query = insert(ReviewInfo).values(
                    pkid=str(uuid4()),
                    movie_id=str(uuid4()),
                    author_id=str(uuid4()),
                    likes_count=0,
                    created=datetime.utcnow(),
                    modified=datetime.utcnow(),
                    review_id=data.context.review_id,
                )
                await db.execute(query)

        query = (
            update(ReviewInfo)
            .where(ReviewInfo.review_id == data.context.review_id)
            .values(
                likes_count=int(data.context.likes),
                modified=data.created_at,
            )
        )
        await db.execute(query)
