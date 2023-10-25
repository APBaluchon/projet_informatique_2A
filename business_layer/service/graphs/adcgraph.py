from business_layer.service.graphs.graph import Graph


class AdcGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "BOTTOM")
        self.indicators = {
            "🏹": {
                "formule": lambda df: (df["totaldamagedealttochampions"] / df["gameduration"]) * 60, 
                "max": 2000, 
                "explication": "Dommages par Minute aux Champions"
            },
            "🌾": {
                "formule": lambda df: (df["totalminionskilled"] / df["gameduration"]) * 60, 
                "max": 10, 
                "explication": "CS par Minute"
            },
            "☠️": {
                "formule": lambda df: (df["kills"] + df["assists"]) / (df["deaths"] + 1), 
                "max": 10, 
                "explication": "Efficacité des Combats (Kills + Assists / Deaths)"
            },
            "🎯": {
                "formule": lambda df: df["turretkills"], 
                "max": 10,
                "explication": "Objectifs Pris (Tours détruits)"
            },
            "💰": {
                "formule": lambda df: (df["goldearned"] / df["gameduration"]) * 60, 
                "max": 800, 
                "explication": "Gold par Minute"
            }
        }
        self.calculate_indicators_players()
        self.display_graph()

