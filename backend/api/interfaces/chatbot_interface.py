from abc import ABC, abstractmethod


class ChatBotInterface(ABC):
    @abstractmethod
    def get_response(self):
        raise NotImplementedError

    @abstractmethod
    def get_text(self):
        raise NotImplementedError
