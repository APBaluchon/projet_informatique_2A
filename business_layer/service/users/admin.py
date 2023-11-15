from business_layer.service.users.userbase import UserBase
from business_layer.dao.dbhandler import DBHandler
from business_layer.dao.dbgameshandler import DBGamesHandler
from business_layer.controler.adminview import AdminView


class Admin(UserBase):
        
    def actions(self):
        """
        Implements admin-specific actions.

        This method provides a series of actions that an admin user can perform, such as
        displaying the database or other admin-specific tasks.
        """
        AdminView().clear_screen()
        action = AdminView().ask_action()

        if action == AdminView().actions_dict["1"]:
            DBHandler().display_database()
        elif action == AdminView().actions_dict["2"]:
            DBHandler().update_database()
        elif action == AdminView().actions_dict["3"]:
            DBHandler().delete_account_from_database()
        elif action == AdminView().actions_dict["4"]:
            DBGamesHandler().add_games_to_database()
        elif action == AdminView().actions_dict["5"]:
            quit()
        return self.actions()