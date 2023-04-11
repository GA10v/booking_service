from abc import ABC, abstractmethod
from uuid import UUID

from services.watcher import layer_models, layer_payload


class WatcherRepositoryProtocol(ABC):
    @abstractmethod
    async def get(self) -> list[str | UUID]:
        ...

    @abstractmethod
    async def update(self, data: list[str | UUID]) -> list[layer_models.UpdateStatus]:
        ...

    @abstractmethod
    async def get_by_id(self, data: layer_models.UpdateStatus) -> layer_models.DetailAnnouncementResponse:
        ...


class NotificRepositoryProtocol(ABC):
    @abstractmethod
    async def send(self, event_type: layer_payload.EventType, payload: layer_payload.DoneAnnounce) -> None:
        ...
