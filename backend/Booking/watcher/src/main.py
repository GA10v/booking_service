import asyncio

from core.config import settings
from db.db import get_session
from db.redis import get_cache
from services.watcher.repositories.notific_repo import get_notific_repo
from services.watcher.repositories.watcher_repo import get_watcher_repo
from services.watcher.service.watcher import WatcherService


async def run_watcher_service():
    db_session = await get_session()
    cache = get_cache()
    watcher_repo = get_watcher_repo(db_session, cache)
    notific_repo = get_notific_repo(cache)
    watcher_service = WatcherService(repo=watcher_repo, cache=cache, notific_repo=notific_repo)

    while True:
        await watcher_service.run()
        await asyncio.sleep(settings.watcher.sleep)


if __name__ == '__main__':
    asyncio.run(run_watcher_service())
