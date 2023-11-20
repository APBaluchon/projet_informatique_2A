from business_layer.service.graphs.graph import Graph


class AdcGraph(Graph):
    """
    A class representing the ADC graph, inheriting from Graph.

    This class specializes in creating a graph for the ADC role in a game,
    focusing on specific indicators relevant to this role.

    Attributes
    ----------
    indicators : dict
        A dictionary mapping indicator symbols to their respective formulas
        and explanations. Each indicator represents a specific metric relevant
        to the ADC role, such as damage per minute or minions killed.

    Parameters
    ----------
    pseudo : str
        The pseudo of the player for whom the graph is being generated.
    """
    def __init__(self, pseudo):
        """
        Initializes the AdcGraph with specific indicators related
        to the ADC role.

        Calls the initialization of the parent Graph class with the pseudo
        and the specific role 'BOTTOM', and sets up indicators specific to
        the ADC role.
        """
        super().__init__(pseudo, "BOTTOM")
        self.indicators = {
            "💥": {
                "formule": lambda df: (
                    df["totaldamagedealttochampions"] / df["gameduration"]
                ) * 60,
                "max": 2000,
                "explication": "Damage per Minute to Champions",
                "longer_explication": (
                    "Measures the average damage the ADC deals to enemy "
                    "champions per minute, "
                    "reflecting their impact in skirmishes and team fights. "
                    "Calculated by dividing "
                    "total damage to champions by the game duration "
                    "in minutes."
                )
            },
            "🌾": {
                "formule": lambda df: (
                    df["totalminionskilled"] / df["gameduration"]
                ) * 60,
                "max": 10,
                "explication": "Minions killed per Minute",
                "longer_explication": (
                    "Measures the ADC's farming efficiency, indicating their "
                    "ability to acquire gold "
                    "and scale into the late game. Calculated by dividing "
                    "total minions killed by the "
                    "game duration in minutes."
                )
            },
            "☠️": {
                "formule": lambda df: (
                    df["kills"] + df["assists"]
                ) / (df["deaths"] + 1),
                "max": 10,
                "explication": "Fight Efficiency (Kills + Assists / Deaths)",
                "longer_explication": (
                    "This indicator measures the player's efficiency "
                    "in fights. It is calculated by "
                    "adding the number of kills and assists, and then "
                    "dividing by the number of deaths "
                    "plus one. A higher value indicates that the player "
                    "is contributing more to fights "
                    "and dying less."
                )
            },
            "🏰": {
                "formule": lambda df: df["turretkills"]
                / df["gameduration"] * 60,
                "max": 0.16,
                "explication": "Turret kills per Minute",
                "longer_explication": (
                    "Reflects the ADC's role in taking down turrets, "
                    "calculated as the average number "
                    "of turret kills per minute. It shows the player's "
                    "objective-focused gameplay."
                )
            },
            "💰": {
                "formule": lambda df: (
                    df["goldearned"] / df["gameduration"]
                ) * 60,
                "max": 666,
                "explication": "Gold per Minute",
                "longer_explication": (
                    "Indicates the ADC's efficiency in farming and acquiring "
                    "resources per minute. "
                    "High values show effective last-hitting and kill "
                    "participation. Calculated by dividing "
                    "total gold earned by the game duration in minutes."
                )
            }
        }
        self.calculate_indicators_players()
        self.display_graph()
