from business_layer.dao.dbgameshandler import DBGamesHandler
from business_layer.service.other.utils import Utils
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash import Input, Output, ALL
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import dash
import json


class Graph:
    """
    A class representing a graph for data visualization.

    This class provides functionalities to create and manage graphs based on user data.

    Attributes
    ----------
    caroussel : dash_core_components.Carousel
        The carousel containing the player's games.
    games_player : list of Game
        The list of games played by the player.
    games_other : list of Game
        The list of games played by other players in the same rank tier.
    pseudo : str
        The pseudo of the player for whom the graph is being generated.
    poste : str
        The specific in-game position for which the graph is being created.
    rank : str 
        The rank of the player.
    fig : plotly.graph_objs._figure.Figure
        The figure containing the graph.
    indicators : dict
        A dictionary mapping indicator symbols to their respective formulas and explanations.
        Each indicator represents a specific metric relevant to the player's role, such as
        damage per minute or minions killed.
    indicators_cards : dash_bootstrap_components.Accordion
        The accordion containing the explanations for the indicators.
    indicators_players : dict
        A dictionary mapping indicator symbols to their respective values for the player.
    indicators_others : dict
        A dictionary mapping indicator symbols to their respective values for other players in the same rank tier.
    indicators_explain : dict
        A dictionary mapping indicator symbols to their respective explanations.

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
        self.tab_about_game = None

        self.actual_game = None
        self.caroussel = None
        self.datas_board = None
        self.games_player = None
        self.games_other = None
        self.pseudo = pseudo
        self.poste = poste
        self.rank = rank
        self.fig = None
        self.indicators = dict()
        self.indicators_cards = None
        self.indicators_players = dict()
        self.indicators_others = dict()
        self.indicators_explain = dict()
        self.player_puuid = None
        
    def calculate_indicators_players(self):
        """
        Calculate indicators for players based on their in-game performance.

        This method retrieves player and game data, computes various in-game indicators 
        for the player and others in their rank tier, and stores them for further analysis or visualization.
        """

        self.player_puuid = DBGamesHandler().get_puuid(self.pseudo)
        self.rank = DBGamesHandler().get_player_rank(self.pseudo)
        datas = DBGamesHandler().get_games_for_one_position(self.player_puuid, self.poste)
        datas_others = DBGamesHandler().get_all_games_for_one_position_and_one_tier(self.poste, self.rank)

        df, df_means = Utils().convert_datas_to_dataframe(datas)
        self.games_player = Utils().convert_dataframe_to_game_list(df)

        df_others, df_others_means = Utils().convert_datas_to_dataframe(datas_others)
        self.games_other = Utils().convert_dataframe_to_game_list(df_others)

        self.actual_game = self.games_player[0]
        self.game_datas = pd.DataFrame(DBGamesHandler().get_game_datas(self.actual_game.get_matchid()))

        for indicateur, details in self.indicators.items():
            self.indicators_players[indicateur] = Utils().interpolate(details["formule"](df_means), 0, details["max"])
            self.indicators_others[indicateur] = Utils().interpolate(details["formule"](df_others_means), 0, details["max"])
            self.indicators_explain[indicateur] = details["explication"]

    def create_circular_graph(self):
        """
        Create a circular graph based on the indicators for the player and others in their rank tier.
        """
        r_values_player = list(self.indicators_players.values())
        theta_values_player = list(self.indicators_players.keys())
        r_values_player.append(r_values_player[0])
        theta_values_player.append(theta_values_player[0])
        fig_player = go.Scatterpolar(
            r=r_values_player, 
            theta=theta_values_player, 
            fill='toself', 
            name=f"{self.pseudo}"
        )
        self.fig.add_trace(fig_player)

        r_values_others = list(self.indicators_others.values())
        theta_values_others = list(self.indicators_others.keys())
        r_values_others.append(r_values_others[0])
        theta_values_others.append(theta_values_others[0])
        fig_others = go.Scatterpolar(
            r=r_values_others, 
            theta=theta_values_others, 
            fill='toself', 
            name=self.rank
        )
        self.fig.add_trace(fig_others)

    def create_accordion(self):
        """
        Create an accordion to display explanations for the indicators.
        """
        self.indicators_cards = dbc.Accordion( [
            dbc.AccordionItem(
                title=f'{key} : {val["explication"]}',
                children=[
                    html.P(val["longer_explication"])
                ]
            )
            for key, val in self.indicators.items()
        ])

    def create_carousel(self):
        carousel_items = []
        for game in self.games_player:
            if game.get_matchid() == "":
                continue

            button_class = "game-button-loss" if not game.get_win() else "game-button"

            card_item = html.Div([
                dbc.Button(
                    dbc.Card([
                        dbc.CardImg(
                            src=f"https://ddragon.leagueoflegends.com/cdn/13.22.1/img/champion/{game.get_championname()}.png", 
                            className="custom-card-img",
                            style={"width": "100px", "height": "100px", "object-fit": "cover"}
                        ),
                        dbc.CardBody([
                            html.P(f'{game.get_kills()}/{game.get_deaths()}/{game.get_assists()}'),
                        ])
                    ]),
                    color="link",
                    id={"type": "game-button", "index": game.get_matchid()},
                    n_clicks=0,
                    className=button_class)
            ], style={"display": "inline-block", "margin": "0"})

            carousel_items.append(card_item)

        self.carousel = html.Div(carousel_items, style={
        "display": "flex", 
        "overflowX": "auto"})

    def create_table(self):
        win_color_head = "rgba(50, 255, 100, 0.2)"
        loose_color_head = "rgba(255, 50, 100, 0.2)"

        win_color_row = "rgba(50, 255, 100, 0.1)"
        loose_color_row = "rgba(255, 50, 100, 0.1)"

        gameduration_minutes = self.actual_game.get_gameduration() // 60
        gameduration_seconds = self.actual_game.get_gameduration() % 60

        table_header = [
            html.Thead([
                html.Tr(
                    html.H3(f'{self.actual_game.get_matchid()} - {gameduration_minutes}m{gameduration_seconds}s')
                ),
                html.Tr(
                    [html.Th("")] + 
                    [
                        html.Th(html.Img(src=f"https://ddragon.leagueoflegends.com/cdn/13.22.1/img/champion/{col}.png", alt="Champion Image", style = {"width":"50%", "height":"50%"}), style={"background-color": win_color_head if win else loose_color_head})
                        for col, win in zip(self.game_datas["championname"], self.game_datas["win"])
                    ]
                )
            ]),
        ]

        rows = []
        available = ["kills", "assists", "deaths", "totaldamagedealttochampions", "totalminionskilled", "turretkills", "goldearned"]
        for col in available:
            rows.append(html.Tr([html.Th(col)] + 
                            [
                                html.Td(kill, style={"background-color": win_color_row if win else loose_color_row})
                                for kill, win in zip(self.game_datas[col], self.game_datas["win"])
                            ]
                        ))

        table_body = [html.Tbody(rows)]

        table = dbc.Table(table_header + table_body)
        self.tab_about_game = table

    def setup_callbacks(self, app):
        @app.callback(
            Output('tab-game', 'children'),
            [Input({'type': 'game-button', 'index': ALL}, 'n_clicks')]
        )
        def update_tab_about_game(n_clicks):
            ctx = dash.callback_context
            if not ctx.triggered:
                return self.tab_about_game
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                game_id = json.loads(button_id)["index"]

                self.actual_game = next((game for game in self.games_player if game.get_matchid() == game_id), None)
                self.game_datas = pd.DataFrame(DBGamesHandler().get_game_datas(self.actual_game.get_matchid()))

                self.create_table()
                return self.tab_about_game

    def display_graph(self):
        """
        Display the graph in a Dash application.
        """
        app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
        load_figure_template("VAPOR")

        self.fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'polar'}]])
        self.create_circular_graph()
        self.create_accordion()
        self.create_carousel()
        self.create_table()

        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.Img(src="assets/logo.png", className="logo"), width=12),
            ]),
            dbc.Row([
                dbc.Col(html.H2(f"{self.poste} performance for {self.pseudo}", className = "subtitle"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="graph", figure=self.fig), className = "graph-container", width=6),
                dbc.Col(self.indicators_cards, width=6)
            ]),
            dbc.Row(
                dbc.Col(html.Div(self.carousel), width=12)
            ),
            dbc.Row(
                dbc.Col(self.tab_about_game, id="tab-game")
            )
        ])

        self.setup_callbacks(app)
        app.run_server()
