from users.userbase import UserBase
from inputhandler.inputhandler import InputHandler
from dao.dbgameshandler import DBGamesHandler


class User(UserBase):

    def __init__(self):
        self.actions_dict = {
            "1" : "Analyser un poste",
            "2" : "Quitter l'application"
        }

        self.postes_dict = {
            "1" : "Top",
            "2" : "Jungler",
            "3" : "Mid",
            "4" : "Adc",
            "5" : "Support"
        }

    def display_actions(self, dico):
        for key, value in dico.items():
            print(f"{key} - {value}")
        
    def actions(self):
        InputHandler.clear_screen()
        self.display_actions(self.actions_dict)
        action = InputHandler.get_integer_input("Entrez l'action à réaliser : ", 1, 2)
        InputHandler.clear_screen()

        if action == 1:
            self.generate_graph()
        elif action == 2:
            quit()

        self.actions()

    def generate_graph(self):
        InputHandler.clear_screen()
        pseudo_to_analyze = InputHandler.get_input("Entrez le pseudo du joueur à analyser : ")
        DBGamesHandler.update_database(pseudo_to_analyze)
        self.display_actions(self.postes_dict)
        poste = InputHandler.get_integer_input("Entrez le poste à analyser : ", 1, 5)
        if poste==1:
            pass
