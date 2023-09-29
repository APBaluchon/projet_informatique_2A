from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd


class JunglerGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "JUNGLE")
   
    def calculate_indicators_players(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "JUNGLE")
        df = self.convert_datas_to_dataframe(datas)
        self.indicators_players["🏹"] = self.interpolate((df["kills"]+df["assists"])/(df["deaths"]+1),0, 10)
        self.indicators_players["🌳"] = self.interpolate((df["neutralminionskilled"]+df["totalneutralminions"]+df["teamneutralminionskilled"])/df["gameduration"]*60,0,10)
        self.indicators_players["🎯"] = (df["epicmonsterskilled"]+df["totalepicmonsterskilled"])*60/df["gameduration"]
        self.indicators_players["👁️‍🗨️"] = self.interpolate((df["visionscore"]+df["wardsplaced"]-df["wardskilled"])*60/df["gameduration"], 0, 10)
        self.indicators_players["🌟 "] = self.interpolate((df["kills"]+df["assists"]+df["turretkills"]+df["epicmonsterskilled"])/(df["deaths"]+1), 0, 20)

        self.indicators_explain["🏹"] = "Efficacité des ganks"
        self.indicators_explain["🌳"] = "Contrôle de la jungle"
        self.indicators_explain["🎯"] = "Participation aux objectifs"
        self.indicators_explain["👁️‍🗨️"] = "Vision et contrôle de la carte"
        self.indicators_explain["🌟 "] = "Efficacité générale"