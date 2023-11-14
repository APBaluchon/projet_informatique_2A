from business_layer.service.graphs.graph import Graph


class JunglerGraph(Graph):
    def __init__(self, pseudo):
        super().__init__(pseudo, "JUNGLE")
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
   