from services.announcement.repositories import _protocols


class UserMockRepository(_protocols.UserRepositoryProtocol):
    def __init__(self) -> None:
        ...
