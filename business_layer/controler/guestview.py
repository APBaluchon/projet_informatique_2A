from business_layer.controler.view import View


class GuestView(View):
    """
    A class representing the view for a guest user.
    """
    def display_app_name(self):
        """
        Returns an ASCII art representation of the application name.

        Returns
        -------
        str
            The ASCII art representation of the application name.
        """
        ascii_art = """
   ___                       ___           _           
  / _ \__ _ _ __ ___   ___  / _ \___ _ __ (_)_   _ ___ 
 / /_\/ _` | '_ ` _ \ / _ \/ /_\/ _ \ '_ \| | | | / __|
/ /__\ (_| | | | | | |  __/ /__\  __/ | | | | |_| \__ \\
\____/\__,_|_| |_| |_|\___\____/\___|_| |_|_|\__,_|___/
    """
        return ascii_art

    def ask_pseudo(self):
        """
        Asks the user for their pseudo.

        Returns
        -------
        str
            The pseudo entered by the user.
        """
        return super().get_input("Pseudo : ")

    def ask_password(self):
        """
        Asks the user for their password.

        Returns
        -------
        str
            The password entered by the user.
        """
        return super().get_input("Password : ", "password")

    def wrong_password(self):
        """
        Prints an error message when the password is incorrect.
        """
        print("Incorrect password. Please try again.")

