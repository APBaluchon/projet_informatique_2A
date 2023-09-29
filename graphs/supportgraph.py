from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd


class SupportGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "UTILITY")
    
    def calculate_indicators_players(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "UTILITY")
        df = self.convert_datas_to_dataframe(datas)
        
        self.indicators_players["🛡️"] = self.interpolate((df["kills"]+df["assists"])/(df["deaths"]+1), 0, 10)
        self.indicators_players["👁️‍🗨️"] = self.interpolate((df["visionscore"]*60 / df["gameduration"]) * 60, 0, 10) 
        self.indicators_players["🔔"] = self.interpolate(df["wardsplaced"] - df["wardskilled"], 0, 10)  
        self.indicators_players["🎯"] = self.interpolate((df["assists"] / (df["teamkills"] + 1)), 0, 1)  
        self.indicators_players["💰"] = self.interpolate((df["goldearned"]*60 / df["gameduration"]) * 60, 0, 500)  

        self.indicators_explain["🛡️"] = "Efficacité de Protection"
        self.indicators_explain["👁️‍🗨️"] = "Score de Vision par Minute"
        self.indicators_explain["🔔"] = "Gestion des Wards"
        self.indicators_explain["🎯"] = "Participation aux Objectifs"
        self.indicators_explain["💰"] = "Gold par Minute"

