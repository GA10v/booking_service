from typing import Any

from core.logger import get_logger
from db.redis import RedisCache
from services.watcher import layer_models
from services.watcher.repositories.watcher_repo import WatcherSqlachemyRepository

logger = get_logger(__name__)


class WatcherService:
    def __init__(self, repo: WatcherSqlachemyRepository, cache: RedisCache) -> None:
        self.repo = repo
        self.redis = cache
        logger.info('WatcherService init ...')

    async def _get_from_cache(self, key: str) -> Any:
        return await self.redis.get(key)

    async def _set_to_cache(self, key: str, data: Any) -> None:
        await self.redis.set(key, data)

    async def run(self) -> list[layer_models.UpdateStatus]:
        data = await self.repo.get()
        return await self.repo.update(data)
