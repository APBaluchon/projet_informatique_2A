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
                "explication": "Damage per Minute to Champions",
                "longer_explication": "This indicator measures the amount of damage dealt to enemy champions per minute. It is calculated by dividing the total damage dealt to champions by the game duration in minutes, and then multiplying by 60 to get the damage per minute. A higher value indicates that the player is dealing more damage to enemy champions over the course of the game."
            },
            "🌾": {
                "formule": lambda df: (df["totalminionskilled"] / df["gameduration"]) * 60, 
                "max": 10, 
                "explication": "Creeper Score per Minute",
                "longer_explication": "This indicator measures the number of minions killed per minute. It is calculated by dividing the total number of minions killed by the game duration in minutes, and then multiplying by 60 to get the score per minute. A higher value indicates that the player is killing more minions over the course of the game."
            },
            "☠️": {
                "formule": lambda df: (df["kills"] + df["assists"]) / (df["deaths"] + 1), 
                "max": 10, 
                "explication": "Fight Efficiency (Kills + Assists / Deaths)",
                "longer_explication": "This indicator measures the player's efficiency in fights. It is calculated by adding the number of kills and assists, and then dividing by the number of deaths plus one. A higher value indicates that the player is contributing more to fights and dying less."
            },
            "🎯": {
                "formule": lambda df: df["turretkills"], 
                "max": 10,
                "explication": "Objectives Taken (Towers destroyed)",
                "longer_explication": "This indicator measures the number of enemy towers destroyed by the player. A higher value indicates that the player is successfully taking objectives and pushing the enemy team back."
            },
            "💰": {
                "formule": lambda df: (df["goldearned"] / df["gameduration"]) * 60, 
                "max": 800, 
                "explication": "Gold per Minute",
                "longer_explication": "This indicator measures the amount of gold earned per minute. It is calculated by dividing the total gold earned by the game duration in minutes, and then multiplying by 60 to get the gold per minute. A higher value indicates that the player is earning more gold over the course of the game."
            }
        }
        self.calculate_indicators_players()
        self.display_graph()


if __name__ == "__main__":
    AdcGraph("SlolyS")