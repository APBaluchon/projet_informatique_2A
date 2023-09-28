from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd


class TopGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo)
    
    def calculate_indicators(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "TOP")
        df = self.convert_datas_to_dataframe(datas)
        self.indicators["🏆"] = df["resultat"]
        self.indicators["☠️"] = self.interpolate((df["kills"]+df["assists"])/df["deaths"], 0, 10)
        self.indicators["🌾"] = self.interpolate((df["totalminionskilled"]/df["gameduration"])*60, 0, 10)
        self.indicators["🔥"] = self.interpolate((df["totaldamagedealttochampions"]/df["gameduration"])*60, 0, 1300)
        self.indicators["💪"] = (df["kills"]+df["assists"])/df["teamkills"]

        self.indicators_explain["🏆"] = "Winrate"
        self.indicators_explain["☠️"] = "Kda"
        self.indicators_explain["🌾"] = "CS per minute"
        self.indicators_explain["🔥"] = "Damage per minute"
        self.indicators_explain["💪"] = "Kill participation"
