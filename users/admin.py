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
        
    def actions(self):
        InputHandler.clear_screen()
        action = InputHandler.get_list_input("Selectionnez l'action", self.actions_dict.values())

        if action == self.actions_dict["1"]:
            DBHandler.display_database()
        elif action == self.actions_dict["2"]:
            DBHandler.update_database()
        elif action == self.actions_dict["3"]:
            DBHandler.delete_account_from_database()
        elif action == self.actions_dict["4"]:
            quit()
        return self.actions()