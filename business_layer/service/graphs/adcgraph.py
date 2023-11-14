from business_layer.service.graphs.graph import Graph


class AdcGraph(Graph):
    """
    A class representing the ADC graph, inheriting from Graph.

    This class specializes in creating a graph for the ADC role in a game, focusing on
    specific indicators relevant to this role.

    Attributes
    ----------
    indicators : dict
        A dictionary mapping indicator symbols to their respective formulas and explanations.
        Each indicator represents a specific metric relevant to the ADC role, such as
        damage per minute or minions killed.

    Parameters
    ----------
    pseudo : str
        The pseudo of the player for whom the graph is being generated.
    """
    def __init__(self, pseudo):
        """
        Initializes the AdcGraph with specific indicators related to the ADC role.

        Calls the initialization of the parent Graph class with the pseudo and the specific
        role 'BOTTOM', and sets up indicators specific to the ADC role.
        """
        super().__init__(pseudo, "BOTTOM")
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
                "formule": lambda df: df["turretkills"], 
                "max": 10,
                "explication": "Objectives Taken (Towers destroyed)"
            },
            "💰": {
                "formule": lambda df: (df["goldearned"] / df["gameduration"]) * 60, 
                "max": 800, 
                "explication": "Gold per Minute"
            }
        }
        self.calculate_indicators_players()
        self.display_graph()

