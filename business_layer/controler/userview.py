from business_layer.controler.view import View


class UserView(View):
    """
    A class representing the user view.

    Attributes
    ----------
    actions_dict : dict
        A dictionary containing the available actions.
    positions_dict : dict
        A dictionary containing the available positions.
    """

    actions_dict = {
        "1": "Analyze a position",
        "2": "Quit the application"
    }
    positions_dict = {
        "1" : "Top",
        "2" : "Jungler",
        "3" : "Mid",
        "4" : "ADC",
        "5" : "Support"
    }

    def ask_action(self):
        """
        Asks the user for the action to perform.

        Returns
        -------
        str
            The action to perform.
        """
        return super().get_list_input("Enter the action to perform : ", UserView.actions_dict.values())

    def ask_pseudo_for_analyse(self):
        """
        Asks the user for the player's username to analyze.

        Returns
        -------
        str
            The player's username to analyze.
        """
        return super().get_input("Enter a pseudo to analyze : ")

    def ask_for_position(self):
        """
        Asks the user for the position to analyze.

        Returns
        -------
        str
            The position to analyze.
        """
        return super().get_list_input("Enter the position to analyze : ", UserView.positions_dict.values())