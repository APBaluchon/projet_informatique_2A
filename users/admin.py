from users.userbase import UserBase
from inputhandler.inputhandler import InputHandler


class Admin(UserBase):

    def actions(self):
        poste = InputHandler.get_input("Entrez le poste souhaité à analyser: ")
        print(f"Analyse en cours pour le poste: {poste}")