from abc import ABC, abstractmethod
from uuid import UUID

from services.booking import layer_models, layer_payload


class BookingRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, booking_id: str | UUID) -> layer_models.PGBooking:
        """
        :raises NotFoundError
        """
        ...

    @abstractmethod
    async def get_multy(
        self,
        query: layer_payload.APIMultyPayload,
        user_id: str | UUID,
    ) -> list[layer_models.BookingResponse]:
        """
        :raises ValueMissingError
        """
        ...

    @abstractmethod
    async def create(
        self,
        announce: layer_payload.AnnounceToCreate,
        user_id: str | UUID,
    ) -> str | UUID:
        """
        :raises UniqueConstraintError
        """
        ...

    @abstractmethod
    async def update(
        self,
        user_id: str | UUID,
        booking_id: str | UUID,
        new_status: layer_payload.APIUpdatePayload,
    ) -> None:
        """
        :raises NotFoundError:
        :raises UniqueConstraintError:
        """
        ...

    @abstractmethod
    async def delete(
        self,
        booking_id: str | UUID,
    ) -> None:
        """
        :raises NotFoundError
        """
        ...


class UserRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str | UUID) -> layer_models.UserToResponse:
        ...


class RatingRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str | UUID) -> layer_models.RatingToResponse:
        ...


class MovieRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, movie_id: str | UUID) -> layer_models.MovieToResponse:
        ...


class AnnouncementRepositoryProtocol(ABC):
    @abstractmethod
    async def get_by_id(self, announce_id: str | UUID) -> layer_models.AnnounceToResponse:
        """
        :raises NotFoundError
        """
        ...
