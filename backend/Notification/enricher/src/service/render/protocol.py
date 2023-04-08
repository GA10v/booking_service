from abc import ABC, abstractmethod

from models.payloads import payload
from models.template import TemplateFromDB


class RenderProtocol(ABC):
    @abstractmethod
    async def render(self, template: TemplateFromDB, data: payload, **kwargs) -> str:
        ...
