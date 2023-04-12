import abc


class Storage(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass


class Cache(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass
