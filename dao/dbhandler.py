from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from inputhandler.inputhandler import InputHandler
from dao.dbgameshandler import DBGamesHandler
import requests


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
        puuid_player = DBHandler.get_puuid(pseudo)
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"insert into projet_info.utilisateur values ('{pseudo}','{password}', 'user', '{puuid_player}')"
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

                res = cursor.fetchone()["poste"]

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
            print(f'{elt["pseudo"]} - {elt["poste"]}')

        InputHandler.get_input("Appuyer sur une touche pour revenir au menu : ")

    @classmethod
    def update_database(cls):
        pseudo_compte = InputHandler.get_input("Pseudo du compte à modifier : ")

        while not DBHandler.is_user_in_db(pseudo_compte):
            print("Le pseudo n'est pas dans la base de données.")
            pseudo_compte = InputHandler.get_input("Pseudo du compte à modifier : ")
        
        info_to_update = InputHandler.get_integer_input("1 - Modifier le mdp \n2 - Modifier le rôle\nChoix : ", 1, 2)
        if info_to_update == 1:
            DBHandler.update_password(pseudo_compte)
        elif info_to_update == 2:
            DBHandler.update_role(pseudo_compte)

    @classmethod
    def update_password(cls, pseudo_compte):
        new_password = InputHandler.get_input("Entrer le nouveau mot de passe du compte : ")
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


    @classmethod
    def get_puuid(cls, pseudo):
        url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"
        response = requests.get(url, params=DBGamesHandler.params)

        if response.status_code == 200:
            return response.json()["puuid"]
        else:
            False