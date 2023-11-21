from business_layer.service.graphs.graph import Graph


class MidGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "MIDDLE")
        self.indicators = {
            "🔮": {
                "formule": lambda df: (df["spell1casts"] + df["spell2casts"] + df["spell3casts"] + df["spell4casts"]) / df["gameduration"] * 60, 
                "max": 10, 
                "explication": "Spell casts per Minute",
                "longer_explication" : "Reflects the mid laner's activity and engagement in lane by showing the average number of main ability casts per minute. High values indicate aggressive and active lane control."
                },
            "⚔️": {
                 "formule": lambda df: (
                    df["kills"] + df["assists"]
                 )/ (df["kills"] +1) ,               
                "max": 10,
                "explication": "Fight Efficiency (kills + assists per death)",
                "longer_explication" : "A metric to evaluate combat performance, balancing kills and assists against deaths. A higher KDA suggests better survival and combat contribution. Calculated as (Kills + Assists) divided by (Deaths + 1) to avoid infinity when deaths are zero.",
            },
            "👁️": {
                "formule": lambda df: df["visionscore"] / df["gameduration"] * 60, 
                "max": 2.5, 
                "explication": "Vision Score per Minute",
                "longer_explication": "Reflects the jungler's contribution to map vision and control, calculated as the average vision score per minute. It includes warding and clearing enemy vision."
            },
            "💥": {
                "formule": lambda df: df["totaldamagedealttochampions"] / df["gameduration"] * 60,
                "max": 1333,
                "explication": "Damage per Minute to Champions",
                "longer_explication" : "Shows the average damage the jungler deals to enemy champions per minute, indicating their impact in skirmishes and team fights."
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
            }
        }
        self.calculate_indicators_players()
        self.display_graph()