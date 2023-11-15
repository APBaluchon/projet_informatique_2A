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
                "explication": "Damage per Minute to Champions",
                "longer_explication": "This indicator measures the amount of damage dealt to enemy champions per minute. It is calculated by dividing the total damage dealt to champions by the game duration and multiplying by 60.",
            },
            "🌾": {
                "formule": lambda df: (df["totalminionskilled"] / df["gameduration"]) * 60, 
                "max": 10, 
                "explication": "Creeper Score per Minute",
                "longer_explication": "This indicator measures the number of minions killed per minute. It is calculated by dividing the total number of minions killed by the game duration and multiplying by 60.",
            },
            "☠️": {
                "formule": lambda df: (df["kills"] + df["assists"]) / (df["deaths"] + 1), 
                "max": 10, 
                "explication": "Fight Efficiency (Kills + Assists / Deaths)",
                "longer_explication": "This indicator measures the player's efficiency in fights. It is calculated by adding the number of kills and assists and dividing by the number of deaths plus one.",
            },
            "🎯": {
                "formule": lambda df: df["resultat"], 
                "max": 1,
                "explication": "Winrate",
                "longer_explication": "This indicator measures the player's win rate. It is calculated by dividing the number of games won by the total number of games played.",
            },
            "🤝": {
                "formule": lambda df: (df["kills"] / df["teamkills"]) , 
                "max": 1, 
                "explication": "Kill participation",
                "longer_explication": "This indicator measures the player's participation in team kills. It is calculated by dividing the number of kills the player participated in by the total number of team kills.",
            }
        }
        self.calculate_indicators_players()
        self.display_graph()