from business_layer.service.graphs.graph import Graph


class TopGraph(Graph):
    """
    A class representing the TOP graph, inheriting from Graph.

    This class specializes in creating a graph for the TOP role in a game,
    focusing on specific indicators relevant to this role.

    Attributes
    ----------
    indicators : dict
        A dictionary mapping indicator symbols to their respective formulas
        and explanations. Each indicator represents a specific metric relevant
        to the TOP role, such asdamage per minute or minions killed.

    Parameters
    ----------
    pseudo : str
        The pseudo of the player for whom the graph is being generated.
    """
    def __init__(self, pseudo):
        """
        Initializes the TopGraph with specific indicators related
        to the TOP role.

        Calls the initialization of the parent Graph class with the
        pseudo and the specific role 'TOP', and sets up indicators
        specific to the TOP role.
        """
        super().__init__(pseudo, "TOP")
        self.indicators = {
            "🏰": {
                "formule": lambda df: (df["damagedealttoturrets"] / df["gameduration"]) * 60, 
                "max": 500, 
                "explication": "Damage to Turrets per Minute",
                "longer_explication": "This measures the average damage dealt to enemy turrets per minute, indicating the top laner's ability to pressure lanes and contribute to objective control. It's calculated by dividing the total damage dealt to turrets by the total game duration in minutes."
            },
            "🛡️": {
                "formule": lambda df: (df["totaldamagetaken"] / df["gameduration"]) * 60, 
                "max": 1000, 
                "explication": "Damage Taken per Minute",
                "longer_explication": "Reflects the average amount of damage absorbed by the top laner per minute, demonstrating their ability to engage in fights and sustain damage. Calculated by dividing the total damage taken by the game duration in minutes."
            },
            "🌾": {
                "formule": lambda df: (df["totalminionskilled"] / df["gameduration"]) * 60, 
                "max": 10, 
                "explication": "Minions Killed per Minute",
                "longer_explication": "Indicates the top laner's efficiency in farming minions per minute. Higher numbers show better lane control and farming skills. It's the total minions killed divided by the game duration in minutes.",
            },
            "⚔️": {
                "formule": lambda df: (df["kills"]+df["assists"])/(df["deaths"]+1), 
                "max": 10,
                "explication": "KDA Ratio",
                "longer_explication": "A metric to evaluate combat performance, balancing kills and assists against deaths. A higher KDA suggests better survival and combat contribution. Calculated as (Kills + Assists) divided by (Deaths + 1) to avoid infinity when deaths are zero.",
            },
            "👁️": {
                "formule": lambda df: (df["wardsplaced"] / df["gameduration"]) * 60 , 
                "max": 1, 
                "explication": "Wards Placed per Minute",
                "longer_explication": "Measures the average number of wards placed per minute, reflecting the player's contribution to team vision and map awareness. Calculated by dividing total wards placed by the game duration in minutes.",
            }
        }
        self.calculate_indicators_players()
        self.display_graph()