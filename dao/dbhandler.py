from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from inputhandler.inputhandler import InputHandler
from dao.dbgameshandler import DBGamesHandler


class DBHandler(metaclass=Singleton):

    @classmethod
    def is_user_in_db(cls, pseudo):
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

    @classmethod
    def create_user(cls, pseudo, password):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"insert into projet_info.utilisateur values ('{pseudo}','{password}', 'user')"
                    )
                connection.commit()
            return True
        except Exception as e:
            print(f"Une erreur est survenue: {e}")
            if connection:
                connection.rollback()
            return False 


    @classmethod
    def is_password_correct(cls, pseudo, password):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )

                res = cursor.fetchone()["mdp"]
        
        return res == password

    @classmethod
    def get_user_role(cls, pseudo):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )

                res = cursor.fetchone()["role"]

        return res

    @classmethod
    def display_database(cls):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u"
                )

                res = cursor.fetchall()
        
        for elt in res:
            print(f'{elt["pseudo"]} - {elt["role"]}')

        InputHandler.get_input("Appuyer sur une Entrée pour revenir au menu")

    @classmethod
    def update_database(cls):
        pseudo_compte = InputHandler.get_input("Pseudo du compte à modifier : ")
        possibilities_dict = {
            "1" : "Password",
            "2" : "Rôle"
        }
        while not DBHandler.is_user_in_db(pseudo_compte):
            print("Le pseudo n'est pas dans la base de données.")
            pseudo_compte = InputHandler.get_input("Pseudo du compte à modifier : ")
        
        info_to_update = InputHandler.get_list_input("Choissiez l'information à modifier :", possibilities_dict.values())
        if info_to_update == possibilities_dict["1"]:
            return DBHandler.update_password(pseudo_compte)
        elif info_to_update == possibilities_dict["2"]:
            return DBHandler.update_role(pseudo_compte)

    @classmethod
    def update_password(cls, pseudo_compte):
        new_password = InputHandler.get_input("Entrer le nouveau mot de passe du compte : ", "password")
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "update projet_info.utilisateur u "
                    f"set mdp = '{new_password}' "
                    f"where u.pseudo = '{pseudo_compte}'"
                )

    @classmethod
    def update_role(cls, pseudo_compte):
        role_dict = {
            "admin" : "user",
            "user" : "admin"
        }
        role_actuel = DBHandler.get_user_role(pseudo_compte)
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "update projet_info.utilisateur u "
                    f"set poste = '{role_dict[role_actuel]}' "
                    f"where u.pseudo = '{pseudo_compte}'"
                )

    @classmethod 
    def delete_account_from_database(cls):
        pseudo_compte = InputHandler.get_input("Pseudo du compte à modifier : ")

        while not DBHandler.is_user_in_db(pseudo_compte):
            print("Le pseudo n'est pas dans la base de données.")
            pseudo_compte = InputHandler.get_input("Pseudo du compte à modifier : ")

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "delete from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo_compte}'"
                )
