from business_layer.controler.view import View


class DBView(View):
    """
    A class representing the view for the database controller.
    """

    def press_enter(self):
        """
        Asks the user to press enter to return to the menu.

        Returns
        -------
        str
            The user's input.
        """
        return super().get_input("Press enter to return to the menu")

    def ask_pseudo(self):
        """
        Asks the user to enter a username.

        Returns
        -------
        str
            The user's input.
        """
        return super().get_input("Pseudo: ")

    def ask_modality(self):
        """
        Asks the user to choose the type of modification to make.

        Returns
        -------
        str
            The user's input.
        """
        possibilities_dict = {
            "1": "Password",
            "2": "Rôle"
        }
        return super().get_list_input(
            "Choose the type of modification: ",
            possibilities_dict.values()
        )

    def ask_new_password(self):
        """
        Asks the user to enter a new password.

        Returns
        -------
        str
            The user's input.
        """
        return super().get_input("Enter the new password: ", "password")

    def wrong_password(self):
        """
        Prints an error message indicating that the username is not in the database.
        """
        return print("Pseudo isn't in the database.")

    def ask_password_new_account(self):
        """
        Asks the user to enter a password for a new account.

        Returns
        -------
        str
            The user's input.
        """
        return super().get_input(
            "Enter a new password to create an account: ",
            "password"
        )
