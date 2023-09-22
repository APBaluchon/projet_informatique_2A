from users.userbase import UserBase
from dao.dbhandler import DBHandler
from inputhandler.inputhandler import InputHandler


class Admin(UserBase):

    def __init__(self):
        self.actions_dict = {
            "1": "Consulter la base de données",
            "2": "Modifier les informations d'un utilisateur de la base de données",
            "3": "Supprimer un utilisateur de la base de données",
            "4": "Quitter l'application"
        }

    def display_actions(self):
        for key, value in self.actions_dict.items():
            print(f"{key} - {value}")
        
    def actions(self):
        InputHandler.clear_screen()
        self.display_actions()
        action = InputHandler.get_integer_input("Entrez l'action à réaliser : ", 1, 4)
        InputHandler.clear_screen()

        if action == 1:
            DBHandler.display_database()
        elif action == 2:
            DBHandler.update_database()
        elif action == 3:
            DBHandler.delete_account_from_database()
        elif action == 4:
            quit()
        self.actions()