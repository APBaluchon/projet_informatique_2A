from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd


class TopGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "TOP")
    
    def calculate_indicators_players(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "TOP")
        df = self.convert_datas_to_dataframe(datas)
        self.indicators_players["🏆"] = df["resultat"]
        self.indicators_players["☠️"] = self.interpolate((df["kills"]+df["assists"])/df["deaths"], 0, 10)
        self.indicators_players["🌾"] = self.interpolate((df["totalminionskilled"]/df["gameduration"])*60, 0, 10)
        self.indicators_players["🔥"] = self.interpolate((df["totaldamagedealttochampions"]/df["gameduration"])*60, 0, 1000)
        self.indicators_players["💪"] = (df["kills"]+df["assists"])/df["teamkills"]

        self.indicators_explain["🏆"] = "Winrate"
        self.indicators_explain["☠️"] = "Kda"
        self.indicators_explain["🌾"] = "CS par minute"
        self.indicators_explain["🔥"] = "Dommages par minute"
        self.indicators_explain["💪"] = "Participation aux kills"
