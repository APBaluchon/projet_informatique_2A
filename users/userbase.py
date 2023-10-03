from abc import ABC, abstractmethod
from inputhandler.inputhandler import InputHandler


class UserBase(ABC):

    def __init__(self):
        self.actions_dict = dict()

    @abstractmethod
    def actions(self):
        pass