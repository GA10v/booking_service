from abc import ABC, abstractmethod
from uuid import UUID

from services.watcher import layer_models


class WatcherRepositoryProtocol(ABC):
    @abstractmethod
    async def get(self) -> list[str | UUID]:
        ...

    @abstractmethod
    async def update(self, data: list[str | UUID]) -> list[layer_models.UpdateStatus]:
        ...
