from users.userbase import UserBase
from inputhandler.inputhandler import InputHandler
from dao.dbgameshandler import DBGamesHandler

class User(UserBase):

    def __init__(self, pseudo):
        self.actions_dict = {
            "1" : "Mettre à jour la base de données",
            "2" : "Analyser un poste",
            "3" : "Quitter l'application"
        }
        self.pseudo = pseudo

    def display_actions(self):
        for key, value in self.actions_dict.items():
            print(f"{key} - {value}")
        
    def actions(self):
        self.display_actions()
        action = InputHandler.get_integer_input("Entrez l'action à réaliser : ", 1, 3)
        InputHandler.clear_screen()

        if action == 1:
            DBGamesHandler.update_database(self.pseudo)

        self.actions()


