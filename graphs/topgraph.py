from graphs.graph import Graph
from dao.dbgameshandler import DBGamesHandler
import pandas as pd
import numpy as np

class TopGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo)
    
    def calculate_indicators(self):
        player_puuid = DBGamesHandler.get_puuid(self.pseudo)
        datas = DBGamesHandler.get_games_for_one_position(player_puuid, "TOP")
        df = self.convert_datas_to_dataframe(datas)
        self.indicators["tpt"] = self.interpolate((df["kills"]+df["assists"])*100/df["teamkills"], 20, 80)
        self.indicators["rr"] = self.interpolate((df["kills"]+df["assists"])/df["deaths"], 0.5, 5)
        self.indicators["ef"] = self.interpolate((df["totalminionskilled"]/df["gameduration"])*60, 4, 8)
        self.indicators["vspm"] = self.interpolate((df["visionscore"]/df["gameduration"])*60, 0.5, 3)
        self.indicators["to"] = self.interpolate(df["neutralminionskilled"]/df["totalneutralminions"], 10, 70)
        print(self.indicators)
        input()
        
    def convert_datas_to_dataframe(self, datas):
        df = pd.DataFrame(datas)    
        df.loc['moyenne'] = df.select_dtypes(np.number).mean()
        df.loc['moyenne', df.select_dtypes('object').columns] = ''

        return df.iloc[-1]

    def display_graph(self):
        pass