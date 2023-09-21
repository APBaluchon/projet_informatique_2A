from abc import ABC, abstractmethod
from inputhandler.inputhandler import InputHandler


class UserBase(ABC):

    def __init__(self, pseudo):
        self.pseudo = pseudo

    @abstractmethod
    def actions(self):
        pass