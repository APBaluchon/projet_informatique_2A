"""
This module provides a class for handling interactions with the database.

This class provides methods to perform various database operations
such as checking if a user exists, creating a new user, etc.
"""
import hashlib
from business_layer.dao.dbconnection import DBConnection
from business_layer.service.singleton.singleton import Singleton
from business_layer.controler.dbview import DBView


class DBHandler(metaclass=Singleton):
    """
    A class that handles interactions with the database.

    This class provides methods to perform various database operations
    such as checking if a user exists, creating a new user, etc.
    """
    def is_user_in_db(self, pseudo):
        """
        Checks if a user exists in the database.

        Parameters
        ----------
        pseudo : str
            The pseudo of the user to check.

        Returns
        -------
        bool
            True if the user exists in the database, False otherwise.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM projet_info.utilisateur u "
                        "WHERE u.pseudo = %s",
                        (pseudo,))
                    res = cursor.fetchone()
                    return bool(res)
        except Exception as e:
            print(f"Error checking user in DB: {e}")
            return False

    def create_user(self, pseudo, password):
        """
        Creates a new user in the database with hashed password.

        Parameters
        ----------
        pseudo : str
            The pseudo of the user to create.
        password : str
            The password of the user to create.

        Returns
        -------
        bool
            True if the user creation is successful, False otherwise.
        """
        if not pseudo or not password:
            print("Invalid pseudo or password.")
            return False

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = (
                        "INSERT INTO projet_info.utilisateur "
                        "VALUES (%s, %s, 'user')"
                    )
                    cursor.execute(query, (pseudo, hashed_password))
                    connection.commit()
                    return True
        except Exception as e:
            print(f"Error creating user in DB: {e}")
            return False

    def is_password_correct(self, pseudo, password):
        """
        Checks if the provided password matches the hashed password
        in the database.

        Parameters
        ----------
        pseudo : str
            The pseudo of the user whose password is being verified.
        password : str
            The password to be verified.

        Returns
        -------
        bool
            True if the password matches the one in the database,
            False otherwise.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT mdp FROM projet_info.utilisateur "
                        "WHERE pseudo = %s",
                        (pseudo,)
                    )
                    res = cursor.fetchone()
                    if res:
                        stored_password = res['mdp']
                        hashed_input_password = hashlib.sha256(
                            password.encode()
                            ).hexdigest()
                        return hashed_input_password == stored_password
                    return False
        except Exception as e:
            print(f"Error verifying password in DB: {e}")
            return False

    def get_user_role(self, pseudo):
        """
        Retrieves the role of a user from the database.

        Parameters
        ----------
        pseudo : str
            The pseudo of the user whose role is being retrieved.

        Returns
        -------
        str
            The role of the user in the database.
            Returns None if the user is not found.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT role FROM projet_info.utilisateur "
                        "WHERE pseudo = %s", (pseudo,))
                    res = cursor.fetchone()
                    return res['role'] if res else None
        except Exception as e:
            print(f"Error retrieving user role from DB: {e}")
            return None

    def display_database(self):
        """
        Displays the list of users in the database.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT pseudo, role FROM projet_info.utilisateur"
                    )
                    users = cursor.fetchall()

            print("User List:")
            for user in users:
                print(f"{user['pseudo']} - {user['role']}")

            DBView().press_enter()
        except Exception as e:
            print(f"Error displaying database: {e}")

    def update_database(self):
        """
        Updates the information of a user in the database.

        This method first prompts for the user's pseudo, and if the pseudo
        exists in the database,
        it then asks which aspect of the user's information should be
        updated (e.g., password, role).
        Based on the choice, it delegates to the appropriate method for
        updating the specific information.
        """
        try:
            pseudo_compte = DBView().ask_pseudo()

            while not self.is_user_in_db(pseudo_compte):
                print("Pseudo isn't in database.")
                pseudo_compte = DBView().ask_pseudo()

            info_to_update = DBView().ask_modality()

            if info_to_update == "Password":
                return self.update_password(pseudo_compte)
            if info_to_update == "Rôle":
                return self.update_role(pseudo_compte)
        except Exception as e:
            print(f"Error updating database: {e}")
            return None

    def update_password(self, pseudo_compte):
        """
        Updates the password for a given user in the database.

        Parameters
        ----------
        pseudo_compte : str
            The pseudo of the user whose password is being updated.
        """
        try:
            new_password = DBView().ask_new_password()
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE projet_info.utilisateur "
                        "SET mdp = %s "
                        "WHERE pseudo = %s", (hashed_password, pseudo_compte))
                    connection.commit()
        except Exception as e:
            print(f"Error updating password in DB: {e}")

    def update_role(self, pseudo_compte):
        """
        Updates the role of a specific user in the database.

        Parameters
        ----------
        pseudo_compte : str
            The pseudo of the user whose role is being updated.

        """
        try:
            role_actuel = self.get_user_role(pseudo_compte)
            if role_actuel is None:
                print(f"No user found with pseudo: {pseudo_compte}")
                return
            new_role = 'admin' if role_actuel == 'user' else 'user'

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE projet_info.utilisateur "
                        "SET role = %s "
                        "WHERE pseudo = %s", (new_role, pseudo_compte))
                    connection.commit()
        except Exception as e:
            print(f"Error updating role in DB: {e}")

    def delete_account_from_database(self):
        """
        Deletes a user account from the database.
        """
        try:
            pseudo_compte = DBView().ask_pseudo()

            if not self.is_user_in_db(pseudo_compte):
                print("Pseudo isn't in database.")
                return

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet_info.utilisateur "
                        "WHERE pseudo = %s", (pseudo_compte,))
                    connection.commit()
                    print("Account deleted with success.")
        except Exception as e:
            print(f"Error deleting account from DB: {e}")

    def create_new_account(self, pseudo):
        """
        Creates a new user account in the database.

        Parameters
        ----------
        pseudo : str
            The pseudo for the new user account.

        Returns
        -------
        Bool
            True is account has beed created, otherwise False.
        """
        try:
            password = DBView().ask_password_new_account()
            while (len(password) < 5):
                print("Password must be at least 5 characters long.")
                password = DBView().ask_password_new_account()

            confirm_password = DBView().ask_confirm_password()

            while (password != confirm_password):
                print("Passwords don't match.")
                password = DBView().ask_password_new_account()
                confirm_password = DBView().ask_confirm_password() 

            if self.is_user_in_db(pseudo):
                print("This user already exists.")
                return False

            if self.create_user(pseudo, password):
                print("Account has been created with success !")
                return True
            print("Account creation has failed.")
            return False

        except Exception as e:
            print(f"Creation failed : {e}")
            return False
