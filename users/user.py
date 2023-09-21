from users.userbase import UserBase
from inputhandler.inputhandler import InputHandler

class User(UserBase):

    def __init__(self, pseudo):
        self.actions_dict = {
            "1": "Toplane",
            "2": "Jungler",
            "3": "Mid",
            "4": "Adc",
            "5": "Support"
        }
        self.pseudo = pseudo

    def display_actions(self):
        for key, value in self.actions_dict.items():
            print(f"{key} - {value}")
        
    def actions(self):
        self.display_actions()
        poste = InputHandler.get_integer_input("Entrez le poste souhaité à analyser: ", 1, 5)
        poste_name = self.actions_dict.get(str(poste), "Poste inconnu")

        print(f"Analyse en cours pour le poste: {poste_name}")


