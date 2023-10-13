from view.guestview import GuestView
from dao.dbhandler import DBHandler
from users.user import User
from users.admin import Admin

from view.view import View

class App:
    
    def __init__(self):
        self.pseudo = None
        self.password = None

    def ask_for_pseudo(self):
        GuestView().clear_screen()
        
        self.pseudo = GuestView().ask_pseudo()

        if DBHandler().is_user_in_db(self.pseudo):
            return self.ask_for_password()
        else:
            self.password = DBHandler().create_new_account(self.pseudo)
            return self.handle_user_actions()

    def ask_for_password(self):
        GuestView().clear_screen()
        self.password = GuestView().ask_password()

        while not DBHandler().is_password_correct(self.pseudo, self.password):
            GuestView().wrong_password()
            self.password = GuestView().ask_password()

        return self.handle_user_actions()

    def handle_user_actions(self):
        GuestView().clear_screen()
        role = DBHandler().get_user_role(self.pseudo)

        instance = Admin() if role == "admin" else User()
        return instance.actions()

    def run(self):
        GuestView().clear_screen()
        return self.ask_for_pseudo()


if __name__ == "__main__":
    app = App()
    app.run()