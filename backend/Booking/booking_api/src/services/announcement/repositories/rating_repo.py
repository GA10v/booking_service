from services.announcement.repositories import _protocols


class RatingMockRepository(_protocols.RatingRepositoryProtocol):
    def __init__(self) -> None:
        ...
