from dao.dbconnection import DBConnection
from singleton.singleton import Singleton


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