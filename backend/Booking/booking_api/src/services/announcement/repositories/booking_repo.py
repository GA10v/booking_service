from services.announcement.repositories import _protocols


class BookingSqlachemyRepository(_protocols.BookingRepositoryProtocol):
    def __init__(self) -> None:
        ...
