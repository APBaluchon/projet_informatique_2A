from business_layer.dao.dbgameshandler import DBGamesHandler
from business_layer.service.other.utils import Utils
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Graph:

    def __init__(self, pseudo, poste, rank = None):
        self.pseudo = pseudo
        self.poste = poste
        self.rank = rank
        self.initialize_data_frames()
        self.indicators = dict()
        self.indicators_players = dict()
        self.indicators_others = dict()
        self.indicators_explain = dict()

    def calculate_indicators_players(self):
        player_puuid = DBGamesHandler().get_puuid(self.pseudo)
        self.rank = DBGamesHandler().get_player_rank(self.pseudo)
        datas = DBGamesHandler().get_games_for_one_position(player_puuid, self.poste)
        datas_others = DBGamesHandler().get_all_games_for_one_position_and_one_tier(self.poste, self.rank)
        self.df, self.df_means = Utils().convert_datas_to_dataframe(datas)
        self.df_others, self.df_others_means = Utils().convert_datas_to_dataframe(datas_others)

        for indicateur, details in self.indicators.items():
            self.indicators_players[indicateur] = Utils().interpolate(details["formule"](self.df_means), 0, details["max"])
            self.indicators_others[indicateur] = Utils().interpolate(details["formule"](self.df_others_means), 0, details["max"])
            self.indicators_explain[indicateur] = details["explication"]

    def initialize_data_frames(self):
        self.df = pd.DataFrame()
        self.df_means = pd.DataFrame()
        self.df_others = pd.DataFrame()
        self.df_others_means = pd.DataFrame()

    def create_figures(self):
        fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'polar'}]])
        
        r_values_player = list(self.indicators_players.values())
        theta_values_player = list(self.indicators_players.keys())
        r_values_player.append(r_values_player[0])
        theta_values_player.append(theta_values_player[0])
        fig_player = go.Scatterpolar(
            r=r_values_player, 
            theta=theta_values_player, 
            fill='toself', 
            name=f"{self.pseudo}",
            line=dict(color='#1f77b4')
        )
        fig.add_trace(fig_player)

        r_values_others = list(self.indicators_others.values())
        theta_values_others = list(self.indicators_others.keys())
        r_values_others.append(r_values_others[0])
        theta_values_others.append(theta_values_others[0])
        fig_others = go.Scatterpolar(
            r=r_values_others, 
            theta=theta_values_others, 
            fill='toself', 
            name=self.rank,
            line=dict(color='#ff7f0e')
        )
        fig.add_trace(fig_others)

        return fig

    def display_graph(self):
        app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        
        fig = self.create_figures()
        #indicators_cards = self.create_indicators_cards()
        #carousel = self.create_carousel()

        app.layout = dbc.Container([
            dbc.Col(dcc.Graph(id="graph", figure=fig, className="custom-graph-container"), width=6)
        ])

        app.run_server()