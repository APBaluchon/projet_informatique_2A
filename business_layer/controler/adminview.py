from business_layer.controler.view import View


class AdminView(View):
    """
    This class represents the view for the admin user. It inherits from the View class.
    It contains methods to ask for user input and display information to the user.
    """

    actions_dict = {
            "1": "Consult the database",
            "2": "Modify the information of a user in the database",
            "3": "Delete a user from the database",
            "4": "Add information to the party database",
            "5": "Quit the application"
    }
    choix_dict = {
        "1" : "Add a specific player",
        "2" : "Add players of a rank"
    }
    tier_dict = {
        "1" : "IRON",
        "2" : "BRONZE",
        "3" : "SILVER",
        "4" : "GOLD",
        "5" : "PLATINUM",
        "6" : "EMERALD",
        "7" : "DIAMOND",
    }
    division_dict = {
        "1" : "I",
        "2" : "II",
        "3" : "III",
        "4" : "IV"
    }

    def ask_action(self):
        """
        Asks the user to choose an action from a list of available actions.

        Returns
        -------
        str
            The chosen action.
        """
        return super().get_list_input("Choose an action: ", AdminView().actions_dict.values())

    def ask_pseudo_to_add(self):
        """
        Asks the user to enter the username of the player to add.

        Returns
        -------
        str
            The username of the player to add.
        """
        return super().get_input("Enter the username of the player to add: ")
    
    def ask_tier_to_add(self):
        """
        Asks the user to choose a rank from a list of available ranks.

        Returns
        -------
        str
            The chosen rank.
        """
        return super().get_list_input("Choose the rank: ", AdminView().tier_dict.values())

    def ask_division_to_add(self):
        """
        Asks the user to choose a division from a list of available divisions.

        Returns
        -------
        str
            The chosen division.
        """
        return super().get_list_input("Choose the division: ", AdminView().division_dict.values())

    def ask_choice(self):
        """
        Asks the user to choose an action from a list of available actions.

        Returns
        -------
        str
            The chosen action.
        """
        return super().get_list_input("Select an action: ", AdminView().choix_dict.values())
