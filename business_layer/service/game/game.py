class Game:
    """
    Represents a game object with various attributes related
    to in-game performance.
    """

    def __init__(self, game):
        self.assists = game["assists"]
        self.championname = game["championname"]
        self.deaths = game["deaths"]
        self.damagedealttoturrets = game["damagedealttoturrets"]
        self.gameduration = game["gameduration"]
        self.kills = game["kills"]
        self.matchid = game["matchid"]
        self.puuid = game["puuid"]
        self.spell1casts = game["spell1casts"]
        self.spell2casts = game["spell2casts"]
        self.spell3casts = game["spell3casts"]
        self.spell4casts = game["spell4casts"]
        self.timeccingothers = game["timeccingothers"]
        self.totaldamagedealttochampions = game["totaldamagedealttochampions"]
        self.totaldamagetaken = game["totaldamagetaken"]
        self.totalhealsonteammates = game["totalhealsonteammates"]
        self.totalminionskilled = game["totalminionskilled"]
        self.totaldamageshieldedonteammates = game["totaldamageshieldedonteammates"]
        self.turretkills = game["turretkills"]
        self.wardsplaced = game["wardsplaced"]
        self.win = game["win"]

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

    def get_totalminionskilled(self):
        """
        Returns the total number of minions killed in the game.
        """
        return self.totalminionskilled

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
