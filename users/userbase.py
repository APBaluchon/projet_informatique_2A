from abc import ABC, abstractmethod
from inputhandler.inputhandler import InputHandler


class UserBase(ABC):

    def __init__(self, pseudo):
        self.pseudo = pseudo

    @abstractmethod
    def actions(self):
        pass

    def get_integer_input(self, prompt, min, max):
        while True:
            user_input = InputHandler.get_input(prompt)
            try:
                value = int(user_input)
                if min <= value <= max:
                    return value
                else:
                    print(prompt)
            except ValueError:
                print("Veuillez entrer un entier valide.")
