from abc import ABC, abstractmethod


class LogInterface(ABC):
    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError
