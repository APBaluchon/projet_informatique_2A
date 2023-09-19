from users.userbase import UserBase
from dao.dbhandler import DBHandler
from inputhandler.inputhandler import InputHandler


class Admin(UserBase):

    def __init__(self, pseudo):
        self.actions_dict = {
            "1": "Consulter la base de données",
            "2": "Modifier les informations d'un utilisateur de la base de données",
            "3": "Supprimer un utilisateur de la base de données"
        }
        self.pseudo = pseudo

    def display_actions(self):
        for key, value in self.actions_dict.items():
            print(f"{key} - {value}")
        
    def actions(self):
        self.display_actions()
        action = self.get_integer_input("Entrez l'action à réaliser': ", 1, 3)
        action_name = self.actions_dict.get(str(action), "Action inconnue")
        InputHandler.clear_screen()

        if action == 1:
            DBHandler.display_database()
        print("Appuyez sur une touche pour revenir au menu.")