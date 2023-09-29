from abc import ABC, abstractmethod
import plotly.express as px
import pandas as pd
import numpy as np
from dash import html, Dash, dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class Graph(ABC):

    def __init__(self, pseudo, poste):
        self.pseudo = pseudo
        self.poste = poste
        self.indicators_players = dict()
        self.indicators_others = dict()
        self.indicators_explain = dict()
        self.calculate_indicators_players()
        self.display_graph()
        

    @abstractmethod
    def calculate_indicators_players(self):
        pass

    def display_graph(self):
        app = Dash("Analytics")

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig_player = go.Scatterpolar(r = list(self.indicators_players.values()),
                                     theta = list(self.indicators_players.keys()),
                                     fill = "toself",
                                     showlegend=False)

        fig.add_trace(fig_player)
        
        app.layout = html.Div([
            html.H1(f"Analyse des performances de {self.pseudo} pour le {self.poste}", style = {"textAlign" : "center"}),
            dcc.Graph(id="graph", figure = fig),
            html.Ul([html.Li(f"{key} : {val}") for key, val in self.indicators_explain.items()])
        ])

        app.run_server()

    def convert_datas_to_dataframe(self, datas):
        df = pd.DataFrame(datas)    
        df.loc['moyenne'] = df.select_dtypes(np.number).mean()
        df.loc['moyenne', df.select_dtypes('object').columns] = ''

        return df.iloc[-1]

    def interpolate(self, val, before_min, before_max):
        if before_min == before_max:
            return None
        
        if val <= before_min:
            return 0
        if val >= before_max:
            return 1

        proportion = (val - before_min) / (before_max - before_min)
        return proportion

