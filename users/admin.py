from users.userbase import UserBase
from dao.dbhandler import DBHandler
from dao.dbgameshandler import DBGamesHandler
from view.adminview import AdminView


class Admin(UserBase):
        
    def actions(self):
        AdminView().clear_screen()
        action = AdminView().ask_choice()

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