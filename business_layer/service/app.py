from business_layer.controler.guestview import GuestView
from business_layer.dao.dbhandler import DBHandler
from business_layer.service.users.user import User
from business_layer.service.users.admin import Admin


class App:
    """
    A class representing the application.

    Parameters
    ----------
    pseudo : str or None
        The pseudo of the user, initially set to None.
    password : str or None
        The password of the user, initially set to None.

    Example
    -------
    >>> app = App()
    >>> app.run()
    """
    def __init__(self):
        """
        Initialize the App class with default values for pseudo and password.
        """
        self.pseudo = None
        self.password = None

    def ask_for_pseudo(self):
        """
        Requests the pseudo from the user and checks if it exists in the database.

        This method first clears the screen, then asks the user for their pseudo. It checks
        if the pseudo exists in the database. If it exists, its asks for the password, if it doesn't, its creates a new user.
        """
        GuestView().clear_screen()
        
        self.pseudo = GuestView().ask_pseudo()

        if DBHandler().is_user_in_db(self.pseudo):
            return self.ask_for_password()
        else:
            DBHandler().create_new_account(self.pseudo)
            return self.handle_user_actions()

    def ask_for_password(self):
        """
        Requests the password from the user and validates it against the database.

        This method clears the screen and prompts the user to enter their password. 
        It then checks if the entered password is correct for the given pseudo 
        (username). 
        If the password is incorrect, it informs the user and asks for the password again. 
        This process repeats until the correct password is entered.
        """
        GuestView().clear_screen()
        self.password = GuestView().ask_password()

        while not DBHandler().is_password_correct(self.pseudo, self.password):
            GuestView().wrong_password()
            self.password = GuestView().ask_password()

        return self.handle_user_actions()

    def handle_user_actions(self):
        """
        Handles the user actions based on their role.

        This method clears the screen and retrieves the role of the user (either 'admin' or a regular user). 
        Depending on the role, it either creates an instance of the Admin class or the User class. 
        It then invokes the actions method on the created instance.
        """
        GuestView().clear_screen()
        role = DBHandler().get_user_role(self.pseudo)

        instance = Admin() if role == "admin" else User()
        return instance.actions()

    def run(self):
        """
        Initiates the application's execution.

        This method clears the screen and then calls the `ask_for_pseudo` method to start 
        the process of user authentication.
        """
        GuestView().clear_screen()
        return self.ask_for_pseudo()


if __name__ == "__main__":
    app = App()
    app.run()