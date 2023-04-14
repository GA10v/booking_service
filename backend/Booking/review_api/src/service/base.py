from abc import ABC, abstractmethod


class NoificationServiceBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def send(self):
        pass
