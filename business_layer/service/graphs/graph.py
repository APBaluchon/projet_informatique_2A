import pandas as pd
import numpy as np
from business_layer.dao.dbgameshandler import DBGamesHandler
from business_layer.service.other.utils import Utils

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Graph:
    """
    A class representing a graph for data visualization.

    This class provides functionalities to create and manage graphs based on user data.

    Attributes
    ----------
    pseudo : str
        The pseudo of the user for which the graph is being created.
    poste : str
        The in-game position to analyze
    rank : str, optional
        The rank of the player to analyze
    indicators : dict
        A dictionary to store various indicators for the graph about the player.
    indicators_players : dict
        A dictionary to store indicators values for player.
    indicators_others : dict
        A dictionary to store indicators values for tier of the player.
    indicators_explain : dict
        A dictionary to store explanations of items in indicators.

    Parameters
    ----------
    pseudo : str
        The pseudo of the player for whom the graph is being generated.
    poste : str
        The specific in-game position for which the graph is being created.
    rank : str
        The rank of the player.
    """
    def __init__(self, pseudo, poste, rank = None):
        self.pseudo = pseudo
        self.poste = poste
        self.rank = rank
        self.indicators = dict()
        self.indicators_players = dict()
        self.indicators_others = dict()
        self.indicators_explain = dict()
        
    def calculate_indicators_players(self):
        """
        Calculate indicators for players based on their in-game performance.

        This method retrieves player and game data, computes various in-game indicators 
        for the player and others in their rank tier, and stores them for further analysis or visualization.
        """

        player_puuid = DBGamesHandler().get_puuid(self.pseudo)
        self.rank = DBGamesHandler().get_player_rank(self.pseudo)
        datas = DBGamesHandler().get_games_for_one_position(player_puuid, self.poste)
        datas_others = DBGamesHandler().get_all_games_for_one_position_and_one_tier(self.poste, self.rank)
        df, df_means = Utils().convert_datas_to_dataframe(datas)
        df_others, df_others_means = Utils().convert_datas_to_dataframe(datas_others)

        for indicateur, details in self.indicators.items():
            self.indicators_players[indicateur] = Utils().interpolate(details["formule"](df_means), 0, details["max"])
            self.indicators_others[indicateur] = Utils().interpolate(details["formule"](df_others_means), 0, details["max"])
            self.indicators_explain[indicateur] = details["explication"]

    def display_graph(self):
        app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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

        indicators_cards = dbc.Accordion( [
            dbc.AccordionItem(
                title=f'{key} : {val["explication"]}',
                children=[
                    html.P(val["longer_explication"])
                ]
            )
            for key, val in self.indicators.items()
        ]
        )

        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("GameGenius", className="custom-title"), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H2(f"{self.poste} performance for {self.pseudo}", className="custom-subtitle"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="graph", figure=fig, className="custom-graph-container"), width=6),
                dbc.Col(indicators_cards, width=6)
            ])
        ], fluid=True)

        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white', 
            font=dict(
                color='#333',
                family='Roboto, sans-serif',
                size=12
            ),
            polar=dict(
                bgcolor="white", 
                radialaxis=dict(
                    linecolor="#cccccc", 
                    gridcolor="#e6e6e6"  
                ),
                angularaxis=dict(
                    linecolor="#cccccc",
                    gridcolor="#e6e6e6"  
                )
            ),
            legend=dict(
                bgcolor="rgba(255, 255, 255, 0.8)", 
                font=dict(
                    color="#333"
                )
            )
        )

        app.run_server()
        