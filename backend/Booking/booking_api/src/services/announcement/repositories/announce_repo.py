from services.announcement.repositories import _protocols


class AnnounceSqlachemyRepository(_protocols.AnnouncementRepositoryProtocol):
    def __init__(self) -> None:
        ...
