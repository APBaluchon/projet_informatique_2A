from abc import ABC, abstractmethod
from inputhandler.inputhandler import InputHandler


class UserBase(ABC):

    @abstractmethod
    def actions(self):
        pass