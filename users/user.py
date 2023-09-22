from users.userbase import UserBase
from inputhandler.inputhandler import InputHandler
from dao.dbgameshandler import DBGamesHandler

class User(UserBase):

    def __init__(self):
        self.actions_dict = {
            "1" : "Analyser un poste",
            "2" : "Quitter l'application"
        }

    def display_actions(self):
        for key, value in self.actions_dict.items():
            print(f"{key} - {value}")
        
    def actions(self):
        self.display_actions()
        action = InputHandler.get_integer_input("Entrez l'action à réaliser : ", 1, 2)
        InputHandler.clear_screen()

        if action == 1:
            DBGamesHandler.generate_graph()

        self.actions()

