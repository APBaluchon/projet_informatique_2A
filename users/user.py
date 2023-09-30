from users.userbase import UserBase
from inputhandler.inputhandler import InputHandler
from dao.dbgameshandler import DBGamesHandler
from graphs.topgraph import TopGraph
from graphs.junglergraph import JunglerGraph
from graphs.midgraph import  MidGraph
from graphs.supportgraph import SupportGraph
from graphs.adcgraph import AdcGraph


class User(UserBase):

    def __init__(self):
        self.actions_dict = {
            "1" : "Analyser un poste",
            "2" : "Quitter l'application"
        }

        self.postes_dict = {
            "1" : "Top",
            "2" : "Jungler",
            "3" : "Mid",
            "4" : "Adc",
            "5" : "Support"
        }
        
    def actions(self):
        action = InputHandler.get_list_input("Entrez l'action à réaliser : ", self.actions_dict.values())

        if action == self.actions_dict["1"]:
            self.generate_graph()
        elif action == self.actions_dict["2"]:
            quit()

        InputHandler.clear_screen()
        self.actions()

    def generate_graph(self):
        InputHandler.clear_screen()
        pseudo_to_analyze = InputHandler.get_input("Entrez le pseudo du joueur à analyser : ")

        DBGamesHandler.update_database_games(pseudo_to_analyze)

        poste = InputHandler.get_list_input("Entrez le poste à analyser : ", self.postes_dict.values())
        if poste==self.postes_dict["1"]:
            TopGraph(pseudo_to_analyze)
        elif poste==self.postes_dict["2"]:
            JunglerGraph(pseudo_to_analyze)
        elif poste==self.postes_dict["3"]:
            MidGraph(pseudo_to_analyze)
        elif poste==self.postes_dict["4"]:
            AdcGraph(pseudo_to_analyze)
        elif poste==self.poste_dict["5"]:
            SupportGraph(pseudo_to_analyze)
