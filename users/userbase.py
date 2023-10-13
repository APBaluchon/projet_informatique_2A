from abc import ABC, abstractmethod


class UserBase(ABC):

    @abstractmethod
    def actions(self):
        pass