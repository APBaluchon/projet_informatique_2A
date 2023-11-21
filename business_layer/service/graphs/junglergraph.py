from business_layer.service.graphs.graph import Graph


class JunglerGraph(Graph):
    def __init__(self, pseudo):
        super().__init__(pseudo, "JUNGLE")
        self.indicators = {
            "🌿": {
                "formule": lambda df: (df["neutralminionskilled"] / df["gameduration"]) * 60, 
                "max": 4, 
                "explication": "Neutral Minions Killed per Minute",
                "longer_explication" : "Indicates the jungler's efficiency in farming jungle camps, calculated as the average number of neutral minions killed per minute. Higher numbers show better jungle control and resource utilization."
            },
            "🏹": {
                 "formule": lambda df: (
                    df["kills"] + df["assists"]
                 )/ (df["deaths"] + 1),               
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
            "👁️": {
                "formule": lambda df: df["visionscore"] / df["gameduration"] * 60, 
                "max": 2.5, 
                "explication": "Vision Score per Minute",
                "longer_explication": "Reflects the jungler's contribution to map vision and control, calculated as the average vision score per minute. It includes warding and clearing enemy vision."
            },
            "💥": {
                "formule": lambda df: df["totaldamagedealttochampions"] / df["gameduration"] * 60,
                "max": 1000,
                "explication": "Damage per Minute to Champions",
                "longer_explication" : "Shows the average damage the jungler deals to enemy champions per minute, indicating their impact in skirmishes and team fights."
            },
            "🏆": {
                "formule": lambda df: (df["dragonkills"] + df["baronkills"])/df["gameduration"] * 60,
                "max": 0.1, 
                "explication": "Objectives Killed per Minute",
                "longer_explication" : "Represents the jungler's role in securing major objectives (like dragons, barons), calculated as the average number of these objectives secured per minute."
            }
        }
        self.calculate_indicators_players()
        self.display_graph()
   