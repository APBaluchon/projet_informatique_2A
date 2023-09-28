from abc import ABC, abstractmethod
import plotly.express as px
import pandas as pd
import numpy as np
from dash import html, Dash, dcc


class Graph(ABC):

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.indicators = dict()
        self.indicators_explain = dict()
        self.calculate_indicators()
        self.display_graph()

    @abstractmethod
    def calculate_indicators(self):
        pass

    def display_graph(self):
        app = Dash("Analytics")
        df = pd.DataFrame(dict(r = self.indicators.values(),
                               theta = self.indicators.keys()))
        fig = px.line_polar(df, r="r", theta="theta", line_close=True, template="ggplot2")
        fig.update_traces(fill="toself")
        
        app.layout = html.Div([
            html.H1(f"Analyse des performances de {self.pseudo}", style = {"textAlign" : "center"}),
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

