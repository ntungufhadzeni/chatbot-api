from abc import ABC, abstractmethod


class StepInterface(ABC):
    @abstractmethod
    def get_or_create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError
