from abc import ABC, abstractmethod

from models.payloads import payload


class PayloadsProtocol(ABC):
    @abstractmethod
    async def payload(self) -> payload:
        ...
