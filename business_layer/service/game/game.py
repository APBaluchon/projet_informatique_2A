class Game:
    """
    Represents a game object with various attributes related to in-game performance.

    Attributes
    ----------
    assists: int
        The number of assists in the game.
    deaths: int
        The number of deaths in the game.
    damagedealttoturrets: int
        The amount of damage dealt to turrets in the game.
    gameduration: int
        The duration of the game.
    kills: int
        The number of kills in the game.
    matchid: str
        The ID of the game match.
    puuid: str
        The PUUID (Player Universally Unique Identifier) associated with the game.
    totaldamagedealttochampions: int
        The total damage dealt to champions in the game.
    totaldamagetaken: int
        The total damage taken in the game.
    totalminionskilled: int
        The total number of minions killed in the game.
    turretkills: int
        The number of turrets destroyed in the game.
    wardsplaced: int
        The number of wards placed in the game.
    """

    def __init__(self, datas):
        self.assists = datas['assists']
        self.championname = datas['championname']
        self.deaths = datas['deaths']
        self.damagedealttoturrets = datas['damagedealttoturrets']
        self.gameduration = datas['gameduration']
        self.kills = datas['kills']
        self.matchid = datas['matchid']
        self.puuid = datas['puuid']
        self.teamid = datas['teamid']
        self.totaldamagedealttochampions = datas["totaldamagedealttochampions"]
        self.totaldamagetaken = datas['totaldamagetaken']
        self.totalminionskilled = datas['totalminionskilled']
        self.turretkills = datas["turretkills"]
        self.wardsplaced = datas['wardsplaced']
        self.win = datas["win"]

    def get_assists(self):
        """
        Returns the number of assists in the game.
        """
        return self.assists

    def get_championname(self):
        """
        Returns the name of the champion played in the game.
        """
        return self.championname

    def get_deaths(self):
        """
        Returns the number of deaths in the game.
        """
        return self.deaths

    def get_damagedealttoturrets(self):
        """
        Returns the amount of damage dealt to turrets in the game.
        """
        return self.damagedealttoturrets

    def get_gameduration(self):
        """
        Returns the duration of the game.
        
        The duration is expressed in seconds.
        """
        return self.gameduration

    def get_kills(self):
        """
        Returns the number of kills in the game.
        """
        return self.kills

    def get_matchid(self):
        """
        Returns the ID of the game match.
        """
        return self.matchid

    def get_puuid(self):
        """
        Returns the PUUID associated with the game.
        """
        return self.puuid

    def get_totaldamagedealttochampions(self):
        """
        Returns the total damage dealt to champions in the game.
        """
        return self.totaldamagedealttochampions

    def get_totaldamagetaken(self):
        """
        Returns the total damage taken in the game.
        """
        return self.totaldamagetaken

    def get_totalminiomskilled(self):
        """
        Returns the total number of minions killed in the game.
        """
        return self.totalminiomskilled

    def get_turretkills(self):
        """
        Returns the number of turrets destroyed in the game.
        """
        return self.turretkills

    def get_wardsplaced(self):
        """
        Returns the number of wards placed in the game.
        """
        return self.wardsplaced

    def get_win(self):
        """
        Returns whether the player won the game or not.
        """
        return self.win