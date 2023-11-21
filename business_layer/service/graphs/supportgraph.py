from business_layer.service.graphs.graph import Graph


class SupportGraph(Graph):

    def __init__(self, pseudo):
        super().__init__(pseudo, "UTILITY")
        self.indicators = {
            "🤝" : {
                "formule": lambda df : df["assists"] / df["gameduration"] * 60,
                "max" : 0.5,
                "explication" : "Assists per Minute",
                "longer_explication" : "Measures the average number of assists the support secures per minute, reflecting their ability to contribute to team fights and skirmishes. Calculated by dividing total assists by the game duration in minutes."
            },
            "👁️": {
                "formule": lambda df: df["visionscore"] / df["gameduration"] * 60, 
                "max": 2.5, 
                "explication": "Vision Score per Minute",
                "longer_explication": "Reflects the support's contribution to map vision and control, calculated as the average vision score per minute. It includes warding and clearing enemy vision."
            },
            "🛡️":{
                "formule" : lambda df : (df["totaldamageshieldedonteammates"]+df["totalhealsonteammates"]) / df["gameduration"] * 60,
                "max" : 400,
                "explication" : "Heal and Shield per Minute",
                "longer_explication" : "Measures the average amount of healing and shielding the support provides to their teammates per minute, reflecting their ability to protect their team. Calculated by dividing total healing and shielding by the game duration in minutes."
            },
            "⏳" : {
                "formule" : lambda df : df["timeccingothers"],
                "max" : 300,
                "explication" : "Time spent Crowd Controlling",
                "longer_explication" : "Measures the total time the support spends crowd controlling enemy champions, reflecting their ability to engage and disable enemies. Calculated by adding the total time spent crowd controlling enemies."
            },
            "💥": {
                "formule": lambda df: df["totaldamagedealttochampions"] / df["gameduration"] * 60,
                "max": 1333,
                "explication": "Damage per Minute to Champions",
                "longer_explication" : "Shows the average damage the support deals to enemy champions per minute, indicating their impact in skirmishes and team fights."
            }
        }
        self.calculate_indicators_players()
        self.display_graph()