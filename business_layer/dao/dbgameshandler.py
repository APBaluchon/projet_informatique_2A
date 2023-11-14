from business_layer.dao.dbconnection import DBConnection
from business_layer.service.singleton.singleton import Singleton
import requests
from business_layer.controler.adminview import AdminView
from tqdm import tqdm


class DBGamesHandler(metaclass=Singleton):
    """
    A class for handling game data in the database.

    Attributes
    ----------
    params : dict
        A dictionary containing the API key.
    """
    params = {
        "api_key" : "RGAPI-249bedd1-4fa2-4c85-87f6-daab28f5daff"
    }

    def update_database_games(self, pseudo, start=0, count=60, show_progress_bar=True):
        """
        Update the database with the latest games for a given player.

        Parameters
        ----------
        pseudo : str
            The player's summoner name.
        start : int, optional
            The index of the first game to retrieve (default is 0).
        count : int, optional
            The number of games to retrieve (default is 60).
        show_progress_bar : bool, optional
            Whether to show a progress bar (default is True).
        """
        try:
            self.update_database_players(pseudo)
            player_puuid = self.get_puuid(pseudo)
            last_games = self.get_player_games(player_puuid, start, count)
            total_games = len(last_games)
            if show_progress_bar:
                with tqdm(total=total_games) as pbar:
                    for i, game in enumerate(last_games):
                        if not self.is_game_in_database(player_puuid, game):
                            self.add_game_information_to_database(player_puuid, game)
                        pbar.update(1)
            else:
                for game in last_games:
                    if not self.is_game_in_database(player_puuid, game):
                        self.add_game_information_to_database(player_puuid, game)
        except Exception as e:
            print(f"Error updating database games for {pseudo}: {e}")

    def get_puuid(self, pseudo):
        """
        Get the PUUID for a given player.

        Parameters
        ----------
        pseudo : str
            The player's summoner name.

        Returns
        -------
        str
            The player's PUUID.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                try:
                    query = """
                        SELECT puuid
                        FROM projet_info.players
                        WHERE summonername = %s
                    """
                    cursor.execute(query, (pseudo,))
                    res = cursor.fetchone()
                    if res:
                        return res["puuid"]
                except Exception as e:
                    print(f"Error getting PUUID for {pseudo}: {e}")
        url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"
        response = requests.get(url, params=DBGamesHandler.params)
        return response.json()["puuid"]

    def get_player_games(self, puuid, start=0, count=100):
        """
        Get the latest games for a given player.

        Parameters
        ----------
        puuid : str
            The player's PUUID.
        start : int, optional
            The index of the first game to retrieve (default is 0).
        count : int, optional
            The number of games to retrieve (default is 100).

        Returns
        -------
        list of str
            The list of game IDs.
        """
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        try:
            response = requests.get(url, params=DBGamesHandler.params)
            return response.json()
        except Exception as e:
            print(f"Error getting player games for {puuid}: {e}")
            return []

    def is_game_in_database(self, puuid, matchid):
        """
        Check if a game is already in the database.

        Parameters
        ----------
        puuid : str
            The player's PUUID.
        matchid : str
            The ID of the game to check.

        Returns
        -------
        bool
            True if the game is in the database, False otherwise.
        """
        try:
            query = """
                SELECT COUNT(*) as count
                FROM projet_info.games g
                WHERE g.puuid = %s AND g.matchid = %s
            """
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (puuid, matchid))
                    res = cursor.fetchone()["count"]
            return res == 1
        except Exception as e:
            print(f"Error checking if game {matchid} is in database for {puuid}: {e}")
            return False

    def get_games_for_one_position(self, puuid, poste):
        """
        Get all games for a given player and position.

        Parameters
        ----------
        puuid : str
            The player's PUUID.
        poste : str
            The position to filter by.

        Returns
        -------
        list of dict
            The list of games.
        """
        try:
            query = """
                SELECT *
                FROM projet_info.games g
                WHERE g.puuid = %s AND g.poste = %s
            """
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (puuid, poste))
                    res = cursor.fetchall()
            return res
        except Exception as e:
            print(f"Error getting games for {puuid} and position {poste}: {e}")
            return []

    def get_all_games_for_one_position_and_one_tier(self, poste, tier):
        """
        Get all games for a given position and tier.

        Parameters
        ----------
        poste : str
            The position to filter by.
        tier : str
            The tier to filter by.

        Returns
        -------
        list of dict
            The list of games.
        """
        try:
            query = """
                SELECT *
                FROM projet_info.games g 
                JOIN projet_info.players p ON g.puuid = p.puuid
                WHERE g.poste = %s AND p.rang = %s
            """
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (poste, tier))
                    res = cursor.fetchall()
            return res
        except Exception as e:
            print(f"Error getting games for position {poste} and tier {tier}: {e}")
            return []

    def add_game_information_to_database(self, puuid, matchid):
        """
        Add game information to the database.

        Parameters
        ----------
        puuid : str
            The player's PUUID.
        matchid : str
            The ID of the game to add.
        """
        infos = self.get_all_variables_for_database(puuid, matchid)
        if infos["mapId"] == 11:
            try:
                query = """
                    INSERT INTO projet_info.games (puuid, matchid, poste, resultat, gameDuration, kills, assists, deaths, epicMonstersKilled, totalMinionsKilled, visionScore, neutralMinionsKilled, turretKills, totalDamageDealtToChampions, goldEarned, wardsKilled, wardsPlaced, teamKills, totalNeutralMinions, totalEpicMonstersKilled, teamNeutralMinionsKilled)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(query, (infos["puuid"], infos["matchId"], infos["poste"], infos["resultat"], infos["gameDuration"], infos["kills"], infos["assists"], infos["deaths"], infos["epicMonstersKilled"], infos["totalMinionsKilled"], infos["visionScore"], infos["neutralMinionsKilled"], infos["turretKills"], infos["totalDamageDealtToChampions"], infos["goldEarned"], infos["wardsKilled"], infos["wardsPlaced"], infos["teamKills"], infos["totalNeutralMinions"], infos["totalEpicMonstersKilled"], infos["teamNeutralMinionsKilled"]))
            except Exception as e:
                print(f"Error adding game {matchid} information to database for {puuid}: {e}")

    def get_all_variables_for_database(self, puuid, matchid):
        """
        Get all game variables for a given player and game.

        Parameters
        ----------
        puuid : str
            The player's PUUID.
        matchid : str
            The ID of the game to retrieve.

        Returns
        -------
        dict
            A dictionary containing all game variables.
        """
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchid}"
        response = requests.get(url, params=DBGamesHandler.params)

        if response.status_code != 200:
            return False
        else:
            response = response.json()

        info_about_player = None
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                info_about_player = participant
                break

        infos_response = {
                "mapId" : response["info"]["mapId"],
                "puuid" : info_about_player["puuid"],
                "resultat" : 1 if info_about_player["win"] else 0,
                "matchId" : response["metadata"]["matchId"],
                "poste" : info_about_player["individualPosition"],
                "gameDuration" : response["info"]["gameDuration"],
                "kills" : info_about_player["kills"],
                "assists" : info_about_player["assists"],
                "deaths" : info_about_player["deaths"],
                "epicMonstersKilled" : info_about_player["dragonKills"]+info_about_player["baronKills"],
                "totalMinionsKilled" :info_about_player["totalMinionsKilled"],
                "visionScore" : info_about_player["visionScore"],
                "neutralMinionsKilled" : info_about_player["neutralMinionsKilled"],
                "turretKills" : info_about_player["turretKills"],
                "totalDamageDealtToChampions" : info_about_player["totalDamageDealtToChampions"],
                "goldEarned" : info_about_player["goldEarned"],
                "wardsKilled" : info_about_player["wardsKilled"],
                "wardsPlaced" : info_about_player["wardsPlaced"],
                "teamKills" : 0,
                "totalNeutralMinions" : 0,
                "totalEpicMonstersKilled" : 0,
                "teamNeutralMinionsKilled" : 0,
            }
        
        for participant in response["info"]["participants"]:
            infos_response["teamKills"] += participant["kills"]
            infos_response["totalNeutralMinions"] += participant["neutralMinionsKilled"]
            infos_response["totalEpicMonstersKilled"] += participant["dragonKills"]+participant["baronKills"]
            if participant["teamId"] == info_about_player["teamId"]:
                infos_response["teamNeutralMinionsKilled"] += participant["neutralMinionsKilled"]

        return infos_response

    def get_player_id(self, pseudo):
        """
        Get the player ID for a given player name.

        Parameters
        ----------
        pseudo : str
            The player's name.

        Returns
        -------
        str or None
            The player's ID, or None if the API request failed.
        """
        url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"
        response = requests.get(url, params=DBGamesHandler.params)
        if response.status_code == 200:
            return response.json()["id"]
        else:
            print(f"Error getting player ID for {pseudo}: {response.status_code}")
            return None

    def get_player_rank(self, pseudo):
        """
        Get the player rank for a given player name.

        Parameters
        ----------
        pseudo : str
            The player's name.

        Returns
        -------
        str or None
            The player's rank, or None if the API request failed.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_info.players p WHERE p.summonername = %s",
                    (pseudo,)
                )

                res = cursor.fetchone()
        if res:
            return res["rang"]
        else:
            id_player = self.get_player_id(pseudo)
            url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_player}"
            response = requests.get(url, params=DBGamesHandler.params)
            if response.status_code == 200:
                return response.json()[0]["tier"]
            else:
                print(f"Error getting player rank for {pseudo}: {response.status_code}")
                return None

    def add_games_to_database(self):
        """
        Prompt the user to choose an action for adding games to the database.
        """
        action = AdminView().ask_action()
        if action == AdminView().choix_dict["1"]:
            self.add_games_to_database_from_one_player()
        elif action == AdminView().choix_dict["2"]:
            self.add_games_to_database_from_tier()
        else:
            print("Invalid action. Please choose a valid action.")

    def add_games_to_database_from_one_player(self):
        """
        Update the database with games played by a single player.

        This method prompts the user to enter the name of a player, retrieves the player's match history from the Riot Games API,
        and updates the database with information about each game played by the player.
        """
        pseudo = AdminView().ask_pseudo_to_add()
        self.update_database_games(pseudo)

    def add_games_to_database_from_tier(self):
        """
        Update the database with games played by players in a given tier.

        This method prompts the user to enter a tier, retrieves the list of players in that tier from the Riot Games API,
        and updates the database with information about each game played by each player.
        """
        tier = AdminView().ask_tier_to_add()
        division = AdminView().ask_division_to_add()

        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page=1"
        response = requests.get(url, params=DBGamesHandler.params)

        if response.status_code == 200:
            players = response.json()
            total_players = len(players)
            with tqdm(total=total_players) as pbar:
                for player in players:
                    self.update_database_games(player["summonerName"], 0, 1, False)
                    pbar.update(1)
        else:
            print(f"Error getting players in tier {tier}: {response.status_code}")

    def update_database_players(self, pseudo):
        """
        Update the database with information about a player.

        This method takes a player's summoner name as input, retrieves their rank and PUUID from the Riot Games API,
        and updates the database with this information if the player is not already in the database.

        Parameters
        ----------
        pseudo: str
            The summoner name of the player to update.
        """
        res = 1
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) AS count FROM projet_info.players p "
                    "WHERE p.summonername = %s",
                    (pseudo,)
                )

                res = cursor.fetchone()["count"]

        if res == 0:
            rank = self.get_player_rank(pseudo)
            puuid = self.get_puuid(pseudo)
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO projet_info.players VALUES (%s, %s, %s)",
                        (puuid, pseudo, rank)
                    )