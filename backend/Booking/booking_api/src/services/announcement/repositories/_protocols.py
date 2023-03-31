from abc import ABC, abstractmethod
from uuid import UUID

from services.announcement import layer_models, layer_payload


class AnnouncementRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, announce_id: str | UUID) -> layer_models.DetailAnnouncementResponse:
        """
        :raises NotFoundError
        """
        ...

    @abstractmethod
    async def get_multy(self, query: layer_payload.APIMultyPayload) -> list[layer_models.AnnouncementResponse]:
        ...

    @abstractmethod
    async def create(
        self,
        new_announce: layer_payload.APICreatePayload,
        movie_id: str | UUID,
        author_id: str | UUID,
    ) -> layer_models.DetailAnnouncementResponse:
        """
        :raises UniqueConstraintError
        """
        ...

    @abstractmethod
    async def update(
        self,
        author_id: str | UUID,
        announce_id: str | UUID,
        update_announce: layer_payload.APIUpdatePayload,
    ) -> layer_models.DetailAnnouncementResponse:
        """
        :raises NotFoundError:
        :raises UniqueConstraintError
        """
        ...

    @abstractmethod
    async def delete(
        self,
        author_id: str | UUID,
        announce_id: str | UUID,
    ) -> None:
        """
        :raises NotFoundError
        """
        ...


class UserRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str | UUID) -> str:
        """
        :raises NotFoundError
        """
        ...

    @abstractmethod
    async def get_subs(self, user_id: str | UUID) -> list[str | UUID]:
        ...


class BookingRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, announce_id: str | UUID) -> list[layer_models.BookingToDetailResponse]:
        ...


class RatingRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str | UUID) -> float:
        ...


class MovieRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, movie_id: str | UUID) -> layer_models.MovieToResponse:
        ...