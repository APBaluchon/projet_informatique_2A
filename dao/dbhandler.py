from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from view.dbview import DBView


class DBHandler(metaclass=Singleton):

    def is_user_in_db(self, pseudo):
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

    def create_user(self, pseudo, password):
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


    def is_password_correct(self, pseudo, password):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )

                res = cursor.fetchone()["mdp"]
        
        return res == password

    def get_user_role(self, pseudo):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )

                res = cursor.fetchone()["role"]

        return res

    def display_database(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u"
                )

                res = cursor.fetchall()
        
        for elt in res:
            print(f'{elt["pseudo"]} - {elt["role"]}')

        DBView().press_enter()

    def update_database(self):
        pseudo_compte = DBView().ask_pseudo()

        while not DBHandler().is_user_in_db(pseudo_compte):
            print("Le pseudo n'est pas dans la base de données.")
            pseudo_compte = DBView.ask_pseudo()
        
        info_to_update = DBView().ask_modality()
        if info_to_update == "Password":
            return DBHandler().update_password(pseudo_compte)
        elif info_to_update == "Rôle":
            return DBHandler().update_role(pseudo_compte)


    def update_password(self, pseudo_compte):
        new_password = DBView().ask_new_password()
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "update projet_info.utilisateur u "
                    f"set mdp = '{new_password}' "
                    f"where u.pseudo = '{pseudo_compte}'"
                )


    def update_role(self, pseudo_compte):
        role_dict = {
            "admin" : "user",
            "user" : "admin"
        }
        role_actuel = DBHandler().get_user_role(pseudo_compte)
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "update projet_info.utilisateur u "
                    f"set poste = '{role_dict[role_actuel]}' "
                    f"where u.pseudo = '{pseudo_compte}'"
                )


    def delete_account_from_database(self):
        pseudo_compte = DBView().ask_pseudo()

        while not DBHandler().is_user_in_db(pseudo_compte):
            DBView().wrong_pseudo()
            pseudo_compte = DBView().ask_pseudo()

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "delete from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo_compte}'"
                )

    def create_new_account(self, pseudo):
        DBView().clear_screen()
        password = DBView().ask_password_new_account()
        if DBHandler().create_user(pseudo, password):
            print("Compte créé avec succès!")
            return password
        else:
            return self.create_new_account()
