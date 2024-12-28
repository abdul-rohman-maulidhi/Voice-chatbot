from abc import ABC, abstractmethod

class ChatbotBase(ABC):
    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def respond(self, text: str):
        pass

    @abstractmethod
    def talk(self, response: str):
        pass
