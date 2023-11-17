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
        self.caroussel = None
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
        self.games_player = Utils().convert_dataframe_to_game_list(df)

        df_others, df_others_means = Utils().convert_datas_to_dataframe(datas_others)
        self.games_other = Utils().convert_dataframe_to_game_list(df_others)

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
            name=f"{self.pseudo}",
            line=dict(color='#1f77b4')
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
            name=self.rank,
            line=dict(color='#ff7f0e')
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
        ], className = "custom-card"
        )

    def create_carousel(self):
        """
        Create a carousel to display the player's games.
        """
        carousel_items = []
        for game in self.games_player:
            kda = round((game.get_kills() + game.get_assists()) / game.get_deaths(), 1) if game.get_deaths() != 0 else "Perfect"
            if(game.get_matchid() == ""):
                continue
            if game.get_win():
                overlay_color = "rgba(50, 255, 100, 0.4)"
            else:
                overlay_color = "rgba(255, 50, 100, 0.4)"
            carousel_items.append(
                html.Div([
                    dbc.Button(
                        dbc.Card(
                            dbc.CardBody([
                                html.Img(src=f"https://ddragon.leagueoflegends.com/cdn/13.22.1/img/champion/{game.get_championname()}.png", className="custom-card-img"),
                                html.Hr(),
                                html.P(f'{game.get_kills()}/{game.get_deaths()}/{game.get_assists()}'),
                            ]),
                            style={"text-align": "center", "background-color": overlay_color, "width": "150px"}
                        ),
                        color="link",
                        className="custom-button",
                        id=f"details-button-{game.get_matchid()}",
                        n_clicks=0
                    )
                ])
            )
        self.carousel = html.Div(carousel_items, className = "carousel")
        

    def display_graph(self):
        """
        Display the graph in a Dash application.
        """
        app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        self.fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'polar'}]])
        self.create_circular_graph()
        self.create_accordion()
        self.create_carousel()

        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("GameGenius", className="custom-title"), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H2(f"{self.poste} performance for {self.pseudo}", className="custom-subtitle"), width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="graph", figure=self.fig, className="custom-graph-container"), width=6),
                dbc.Col(self.indicators_cards, width=6)
            ]),
            dbc.Row(html.Div(self.carousel))
        ])

        self.fig.update_layout(
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
        