from inputhandler.inputhandler import InputHandler
from dao.dbhandler import DBHandler
from users.user import User
from users.admin import Admin

from InquirerPy import prompt
from InquirerPy.validator import NumberValidator


class App:
    
    def __init__(self):
        self.handler = InputHandler()
        self.pseudo = None
        self.password = None

    def ask_for_pseudo(self):
        self.handler.clear_screen()
        
        self.pseudo = self.handler.get_input("Pseudo : ")

        if DBHandler.is_user_in_db(self.pseudo):
            return self.ask_for_password()
        else:
            self.password = DBHandler.create_new_account(self.pseudo)
            return self.handle_user_actions()

    def ask_for_password(self):
        self.handler.clear_screen()
        self.password = self.handler.get_input("Password : ", "password")

        while not DBHandler.is_password_correct(self.pseudo, self.password):
            print("Mot de passe incorrect. Veuillez réessayer.")
            self.password = self.handler.get_input("Password : ", "password")

        return self.handle_user_actions()

    def handle_user_actions(self):
        self.handler.clear_screen()
        role = DBHandler.get_user_role(self.pseudo)

        instance = Admin() if role == "admin" else User()
        return instance.actions()

    def run(self):
        self.handler.clear_screen()
        return self.ask_for_pseudo()


if __name__ == "__main__":
    app = App()
    app.run()