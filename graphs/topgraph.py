from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler

class TopGraph(Graph):

    def calculate_indicators(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "TOP")

    def display_graph(self):
        pass