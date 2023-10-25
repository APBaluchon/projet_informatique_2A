from business_layer.service.users.userbase import UserBase
from business_layer.dao.dbgameshandler import DBGamesHandler
from business_layer.service.graphs.topgraph import TopGraph
from business_layer.service.graphs.junglergraph import JunglerGraph
from business_layer.service.graphs.midgraph import  MidGraph
from business_layer.service.graphs.supportgraph import SupportGraph
from business_layer.service.graphs.adcgraph import AdcGraph
from business_layer.controler.userview import UserView

class User(UserBase):
        
    def actions(self):
        action = UserView().ask_action()

        if action == UserView().actions_dict["1"]:
            self.generate_graph()
        elif action == UserView().actions_dict["2"]:
            quit()

        UserView().clear_screen()
        self.actions()

    def generate_graph(self):
        UserView().clear_screen()
        pseudo_to_analyze = UserView().ask_pseudo_for_analyse()

        DBGamesHandler().update_database_games(pseudo_to_analyze)

        poste = UserView().ask_for_position()
        
        if poste==UserView().positions_dict["1"]:
            TopGraph(pseudo_to_analyze)
        elif poste==UserView().positions_dict["2"]:
            JunglerGraph(pseudo_to_analyze)
        elif poste==UserView().positions_dict["3"]:
            MidGraph(pseudo_to_analyze)
        elif poste==UserView().positions_dict["4"]:
            AdcGraph(pseudo_to_analyze)
        elif poste==UserView().positions_dict["5"]:
            SupportGraph(pseudo_to_analyze)
