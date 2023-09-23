from inputhandler.inputhandler import InputHandler
from dao.dbhandler import DBHandler
from users.user import User
from users.admin import Admin


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
            print("Pseudo non trouvé. Veuillez créer un compte.")
            return self.create_new_account()

    def ask_for_password(self):
        self.handler.clear_screen()
        self.password = self.handler.get_input("Password : ")

        while not DBHandler.is_password_correct(self.pseudo, self.password):
            print("Mot de passe incorrect. Veuillez réessayer.")
            self.password = self.handler.get_input("Password : ")

        return self.handle_user_actions()

    def create_new_account(self):
        self.handler.clear_screen()
        self.password = self.handler.get_input("Entrez un nouveau mot de passe pour créer un compte : ")
        if DBHandler.create_user(self.pseudo, self.password):
            print("Compte créé avec succès!")
            return self.handle_user_actions()
        else:
            return self.create_new_account()

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