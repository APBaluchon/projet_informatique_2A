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
        poste = self.get_integer_input("Entrez le poste souhaité à analyser: ")
        poste_name = self.actions_dict.get(str(poste), "Poste inconnu")

        print(f"Analyse en cours pour le poste: {poste_name}")

    def get_integer_input(self, prompt="Entrez un nombre entre 1 et 5: "):
        while True:
            user_input = InputHandler.get_input(prompt)
            try:
                value = int(user_input)
                if 1 <= value <= 5:
                    return value
                else:
                    print("Veuillez entrer un nombre entre 1 et 5.")
            except ValueError:
                print("Veuillez entrer un entier valide.")
