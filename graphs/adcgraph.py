from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd


class AdcGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "BOTTOM")
    
    def calculate_indicators_players(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "BOTTOM")
        datas_others = DBGamesHandler.get_all_games_for_one_position("BOTTOM")
        df = self.convert_datas_to_dataframe(datas)
        df_others = self.convert_datas_to_dataframe(datas_others)
        
        self.indicators_players["🏹"] = self.interpolate((df["totaldamagedealttochampions"] / df["gameduration"]) * 60, 0, 2000) 
        self.indicators_players["🌾"] = self.interpolate((df["totalminionskilled"] / df["gameduration"]) * 60, 0, 10) 
        self.indicators_players["☠️"] = self.interpolate((df["kills"] + df["assists"]) / (df["deaths"] + 1), 0, 10) 
        self.indicators_players["🎯"] = self.interpolate(df["turretkills"], 0, 10)
        self.indicators_players["💰"] = self.interpolate((df["goldearned"] / df["gameduration"]) * 60, 0, 800) 

        self.indicators_others["🏹"] = self.interpolate((df_others["totaldamagedealttochampions"] / df_others["gameduration"]) * 60, 0, 2000) 
        self.indicators_others["🌾"] = self.interpolate((df_others["totalminionskilled"] / df_others["gameduration"]) * 60, 0, 10) 
        self.indicators_others["☠️"] = self.interpolate((df_others["kills"] + df_others["assists"]) / (df_others["deaths"] + 1), 0, 10) 
        self.indicators_others["🎯"] = self.interpolate(df_others["turretkills"], 0, 10)
        self.indicators_others["💰"] = self.interpolate((df_others["goldearned"] / df_others["gameduration"]) * 60, 0, 800) 
        
        self.indicators_explain["🏹"] = "Dommages par Minute aux Champions"
        self.indicators_explain["🌾"] = "CS par Minute"
        self.indicators_explain["☠️"] = "Efficacité des Combats (Kills + Assists / Deaths)"
        self.indicators_explain["🎯"] = "Objectifs Pris (Tours détruits)"
        self.indicators_explain["💰"] = "Gold par Minute"
 
