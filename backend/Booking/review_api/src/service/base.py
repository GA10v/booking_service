from abc import ABC, abstract_method


class NoificationServiceBase(ABC):

    @abstract_method
    def __init__(self):
        pass

    @abstract_method
    async def send(self):
        pass
