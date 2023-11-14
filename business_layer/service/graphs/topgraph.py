from business_layer.service.graphs.graph import Graph


class TopGraph(Graph):
    """
    A class representing the TOP graph, inheriting from Graph.

    This class specializes in creating a graph for the TOP role in a game, focusing on
    specific indicators relevant to this role.

    Attributes
    ----------
    indicators : dict
        A dictionary mapping indicator symbols to their respective formulas and explanations.
        Each indicator represents a specific metric relevant to the TOP role, such as
        damage per minute or minions killed.

    Parameters
    ----------
    pseudo : str
        The pseudo of the player for whom the graph is being generated.
    """
    def __init__(self, pseudo):
        """
        Initializes the TopGraph with specific indicators related to the TOP role.

        Calls the initialization of the parent Graph class with the pseudo and the specific
        role 'TOP', and sets up indicators specific to the TOP role.
        """
        super().__init__(pseudo, "TOP")
        self.indicators = {
            "🏹": {
                "formule": lambda df: (df["totaldamagedealttochampions"] / df["gameduration"]) * 60, 
                "max": 2000, 
                "explication": "Damage per Minute to Champions"
            },
            "🌾": {
                "formule": lambda df: (df["totalminionskilled"] / df["gameduration"]) * 60, 
                "max": 10, 
                "explication": "Creeper Score per Minute"
            },
            "☠️": {
                "formule": lambda df: (df["kills"] + df["assists"]) / (df["deaths"] + 1), 
                "max": 10, 
                "explication": "Fight Efficiency (Kills + Assists / Deaths)"
            },
            "🎯": {
                "formule": lambda df: df["resultat"], 
                "max": 1,
                "explication": "Winrate"
            },
            "🤝": {
                "formule": lambda df: (df["kills"] / df["teamkills"]) , 
                "max": 800, 
                "explication": "Kill participation"
            }
        }
        self.calculate_indicators_players()
        self.display_graph()