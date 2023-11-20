import os
from InquirerPy import prompt


class View:
    """
    This class represents the View layer of the application. It contains 
    methods for getting user input and clearing the screen.
    """

    def clear_screen(self):
        """
        This method clears the screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_input(self, message, type_message="input"):
        """
        This method prompts the user for input and returns the result.

        Parameters
        ----------
        message: str
            The message to display to the user.
        type_message: str, optional
            The type of input to get from the user. Defaults to "input".

        Returns
        -------
        str
            The user's input.
        """
        questions = [
            {
                "type": type_message,
                "message": message,
                "name": "resultat"
            }
        ]

        result = prompt(questions)
        return result["resultat"]

    def get_list_input(self, message, list_values):
        """
        This method prompts the user to select an item from a list
        and returns the result.

        Parameters
        ----------
        message: str
            The message to display to the user.
        list_values: list
            The list of values to display to the user.

        Returns
        -------
        str
            The user's selected item.
        """
        questions = [
            {
                "type": "list",
                "message": message,
                "choices": list_values,
                "name": "resultat"
            }
        ]

        result = prompt(questions)["resultat"]
        return result
