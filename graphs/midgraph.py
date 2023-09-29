from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd


class MidGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "MIDDLE")
   
    def calculate_indicators_players(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "MIDDLE")
        df = self.convert_datas_to_dataframe(datas)
        self.indicators_players["🥊"] = self.interpolate((df["kills"]+df["assists"])/(df["deaths"]+1), 0, 10)
        self.indicators_players["🛡️"] = self.interpolate(df["totalminionskilled"]*60/df["gameduration"],0,10)
        self.indicators_players["🎯"] = (df["totalepicmonsterskilled"]+df["turretkills"])*60/df["gameduration"]
        self.indicators_players["👁️‍🗨️"] = self.interpolate((df["visionscore"]+df["wardsplaced"]-df["wardskilled"])*60/df["gameduration"],0,10)
        self.indicators_players["⚔️"] = self.interpolate(df["totaldamagedealttochampions"]*60/df["gameduration"], 0, 2000)

        self.indicators_explain["🥊"] = "Ratio de combat"
        self.indicators_explain["🛡️"] = "Ratio de contrôle de lane"
        self.indicators_explain["🎯"] = "Participation aux objectifs"
        self.indicators_explain["👁️‍🗨️"] = "Vision et détection"
        self.indicators_explain["⚔️"] = "Dommages infligés"