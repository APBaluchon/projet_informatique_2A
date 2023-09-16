import os
from dbconnection import DBConnection


class App:

    def __init__(self):
        self.run()

    def run(self):
        pseudo = self.ask_for_pseudo()
        if self.check_if_pseudo_in_ddb(pseudo):
            password = self.ask_for_password()
            if self.check_if_password_is_correct(pseudo, password):
                pass
        else:
            pass

    def ask_for_pseudo(self):
        return input("Pseudo : ")

    def ask_for_password(self):
        return input("Password : ")

    def check_if_pseudo_in_ddb(self, pseudo):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )
                res = cursor.fetchone()
        if res:
            return True
        else:
            return False

    def check_if_password_is_correct(self, pseudo, password):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )
                res = cursor.fetchone()["mdp"]
        return res == password

if __name__ == "__main__":
    App()
