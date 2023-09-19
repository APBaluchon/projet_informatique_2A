from abc import ABC, abstractmethod


class UserBase(ABC):

    def __init__(self, pseudo):
        self.pseudo = pseudo

    @abstractmethod
    def actions(self):
        pass