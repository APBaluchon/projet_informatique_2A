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
        "api_key" : "RGAPI-1458f4dd-9a7c-4c78-9b2a-6d803bacb22f"
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
            AdminView().clear_screen()
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
                WHERE g.puuid = %s AND g.teamposition = %s
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
                WHERE g.teamposition = %s AND p.rang = %s
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
        for info in infos:
            if info["queueId"] in [420, 440]:
                try:
                    query = """
                        INSERT INTO projet_info.games (
                            matchId, puuid, assists, baronKills, bountyLevel, 
                            champExperience, champLevel, championName, consumablesPurchased, 
                            damageDealtToBuildings, damageDealtToObjectives, damageDealtToTurrets, 
                            damageSelfMitigated, deaths, detectorWardsPlaced, doubleKills, 
                            dragonKills, firstBloodAssist, firstBloodKill, firstTowerAssist, 
                            firstTowerKill, gameDuration, gameEndedInEarlySurrender, gameEndedInSurrender, 
                            goldEarned, goldSpent, inhibitorKills, inhibitorTakedowns, 
                            inhibitorsLost, item0, item1, item2, item3, item4, item5, 
                            item6, itemsPurchased, killingSprees, kills, 
                            largestCriticalStrike, largestKillingSpree, largestMultiKill, 
                            longestTimeSpentLiving, magicDamageDealt, magicDamageDealtToChampions, 
                            magicDamageTaken, neutralMinionsKilled, nexusKills, nexusTakedowns, 
                            nexusLost, objectivesStolen, objectivesStolenAssists, participantId, 
                            pentaKills, physicalDamageDealt, physicalDamageDealtToChampions, 
                            physicalDamageTaken, quadraKills, riotIdName, 
                            riotIdTagline, sightWardsBoughtInGame, spell1Casts, 
                            spell2Casts, spell3Casts, spell4Casts, summoner1Casts, 
                            summoner1Id, summoner2Casts, summoner2Id, teamEarlySurrendered, teamId, 
                            teamKills, teamPosition, timeCCingOthers, timePlayed, totalDamageDealt, 
                            totalDamageDealtToChampions, totalDamageShieldedOnTeammates, 
                            totalDamageTaken, totalHeal, totalHealsOnTeammates, totalMinionsKilled, 
                            totalTimeCCDealt, totalTimeSpentDead, totalUnitsHealed, tripleKills, 
                            trueDamageDealt, trueDamageDealtToChampions, trueDamageTaken, 
                            turretKills, turretTakedowns, turretsLost, unrealKills, visionScore, 
                            visionWardsBoughtInGame, wardsKilled, wardsPlaced, win
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(query, (
                                info["matchId"], info["puuid"], info["assists"], info["baronKills"], info["bountyLevel"], 
                                info["champExperience"], info["champLevel"], info["championName"], info["consumablesPurchased"], 
                                info["damageDealtToBuildings"], info["damageDealtToObjectives"], info["damageDealtToTurrets"], 
                                info["damageSelfMitigated"], info["deaths"], info["detectorWardsPlaced"], info["doubleKills"], 
                                info["dragonKills"], info["firstBloodAssist"], info["firstBloodKill"], info["firstTowerAssist"], 
                                info["firstTowerKill"], info["gameDuration"], info["gameEndedInEarlySurrender"], info["gameEndedInSurrender"], 
                                info["goldEarned"], info["goldSpent"], info["inhibitorKills"], info["inhibitorTakedowns"], 
                                info["inhibitorsLost"], info["item0"], info["item1"], info["item2"], info["item3"], info["item4"], info["item5"], 
                                info["item6"], info["itemsPurchased"], info["killingSprees"], info["kills"], 
                                info["largestCriticalStrike"], info["largestKillingSpree"], info["largestMultiKill"], 
                                info["longestTimeSpentLiving"], info["magicDamageDealt"], info["magicDamageDealtToChampions"], 
                                info["magicDamageTaken"], info["neutralMinionsKilled"], info["nexusKills"], info["nexusTakedowns"], 
                                info["nexusLost"], info["objectivesStolen"], info["objectivesStolenAssists"], info["participantId"], 
                                info["pentaKills"], info["physicalDamageDealt"], info["physicalDamageDealtToChampions"], 
                                info["physicalDamageTaken"], info["quadraKills"], info["riotIdName"], 
                                info["riotIdTagline"], info["sightWardsBoughtInGame"], info["spell1Casts"], 
                                info["spell2Casts"], info["spell3Casts"], info["spell4Casts"], info["summoner1Casts"], 
                                info["summoner1Id"], info["summoner2Casts"], info["summoner2Id"], info["teamEarlySurrendered"], info["teamId"], 
                                info["teamKills"], info["teamPosition"], info["timeCCingOthers"], info["timePlayed"], info["totalDamageDealt"], 
                                info["totalDamageDealtToChampions"], info["totalDamageShieldedOnTeammates"], 
                                info["totalDamageTaken"], info["totalHeal"], info["totalHealsOnTeammates"], info["totalMinionsKilled"], 
                                info["totalTimeCCDealt"], info["totalTimeSpentDead"], info["totalUnitsHealed"], info["tripleKills"], 
                                info["trueDamageDealt"], info["trueDamageDealtToChampions"], info["trueDamageTaken"], 
                                info["turretKills"], info["turretTakedowns"], info["turretsLost"], info["unrealKills"], info["visionScore"], 
                                info["visionWardsBoughtInGame"], info["wardsKilled"], info["wardsPlaced"], info["win"]
                                ))
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

        all_players_info = []

        for participant in response["info"]["participants"]:
            player_info = {
                "queueId": response["info"]["queueId"],
                "mapId": response["info"]["mapId"],
                "matchId": response["metadata"]["matchId"],
                "puuid": participant.get("puuid", ""),
                "assists": participant.get("assists", 0),
                "baronKills": participant.get("baronKills", 0),
                "bountyLevel": participant.get("bountyLevel", 0),
                "champExperience": participant.get("champExperience", 0),
                "champLevel": participant.get("champLevel", 0),
                "championName": participant.get("championName", ""),
                "consumablesPurchased": participant.get("consumablesPurchased", 0),
                "damageDealtToBuildings": participant.get("damageDealtToBuildings", 0),
                "damageDealtToObjectives": participant.get("damageDealtToObjectives", 0),
                "damageDealtToTurrets": participant.get("damageDealtToTurrets", 0),
                "damageSelfMitigated": participant.get("damageSelfMitigated", 0),
                "deaths": participant.get("deaths", 0),
                "detectorWardsPlaced": participant.get("detectorWardsPlaced", 0),
                "doubleKills": participant.get("doubleKills", 0),
                "dragonKills": participant.get("dragonKills", 0),
                "firstBloodAssist": participant.get("firstBloodAssist", False),
                "firstBloodKill": participant.get("firstBloodKill", False),
                "firstTowerAssist": participant.get("firstTowerAssist", False),
                "firstTowerKill": participant.get("firstTowerKill", False),
                "gameDuration": response["info"]["gameDuration"],
                "gameEndedInEarlySurrender": participant.get("gameEndedInEarlySurrender", False),
                "gameEndedInSurrender": participant.get("gameEndedInSurrender", False),
                "goldEarned": participant.get("goldEarned", 0),
                "goldSpent": participant.get("goldSpent", 0),
                "inhibitorKills": participant.get("inhibitorKills", 0),
                "inhibitorTakedowns": participant.get("inhibitorTakedowns", 0),
                "inhibitorsLost": participant.get("inhibitorsLost", 0),
                "item0": participant.get("item0", 0),
                "item1": participant.get("item1", 0),
                "item2": participant.get("item2", 0),
                "item3": participant.get("item3", 0),
                "item4": participant.get("item4", 0),
                "item5": participant.get("item5", 0),
                "item6": participant.get("item6", 0),
                "itemsPurchased": participant.get("itemsPurchased", 0),
                "killingSprees": participant.get("killingSprees", 0),
                "kills": participant.get("kills", 0),
                "largestCriticalStrike": participant.get("largestCriticalStrike", 0),
                "largestKillingSpree": participant.get("largestKillingSpree", 0),
                "largestMultiKill": participant.get("largestMultiKill", 0),
                "longestTimeSpentLiving": participant.get("longestTimeSpentLiving", 0),
                "magicDamageDealt": participant.get("magicDamageDealt", 0),
                "magicDamageDealtToChampions": participant.get("magicDamageDealtToChampions", 0),
                "magicDamageTaken": participant.get("magicDamageTaken", 0),
                "neutralMinionsKilled": participant.get("neutralMinionsKilled", 0),
                "nexusKills": participant.get("nexusKills", 0),
                "nexusTakedowns": participant.get("nexusTakedowns", 0),
                "nexusLost": participant.get("nexusLost", 0),
                "objectivesStolen": participant.get("objectivesStolen", 0),
                "objectivesStolenAssists": participant.get("objectivesStolenAssists", 0),
                "participantId": participant.get("participantId", 0),
                "pentaKills": participant.get("pentaKills", 0),
                "physicalDamageDealt": participant.get("physicalDamageDealt", 0),
                "physicalDamageDealtToChampions": participant.get("physicalDamageDealtToChampions", 0),
                "physicalDamageTaken": participant.get("physicalDamageTaken", 0),
                "quadraKills": participant.get("quadraKills", 0),
                "riotIdName": participant.get("riotIdName", ""),
                "riotIdTagline": participant.get("riotIdTagline", ""),
                "sightWardsBoughtInGame": participant.get("sightWardsBoughtInGame", 0),
                "spell1Casts": participant.get("spell1Casts", 0),
                "spell2Casts": participant.get("spell2Casts", 0),
                "spell3Casts": participant.get("spell3Casts", 0),
                "spell4Casts": participant.get("spell4Casts", 0),
                "summoner1Casts": participant.get("summoner1Casts", 0),
                "summoner1Id": participant.get("summoner1Id", 0),
                "summoner2Casts": participant.get("summoner2Casts", 0),
                "summoner2Id": participant.get("summoner2Id", 0),
                "teamEarlySurrendered": participant.get("teamEarlySurrendered", False),
                "teamId": participant.get("teamId", 0),
                "teamKills": sum([p["kills"] for p in response["info"]["participants"]]),
                "teamPosition": participant.get("teamPosition", ""),
                "timeCCingOthers": participant.get("timeCCingOthers", 0),
                "timePlayed": participant.get("timePlayed", 0),
                "totalDamageDealt": participant.get("totalDamageDealt", 0),
                "totalDamageDealtToChampions": participant.get("totalDamageDealtToChampions", 0),
                "totalDamageShieldedOnTeammates": participant.get("totalDamageShieldedOnTeammates", 0),
                "totalDamageTaken": participant.get("totalDamageTaken", 0),
                "totalHeal": participant.get("totalHeal", 0),
                "totalHealsOnTeammates": participant.get("totalHealsOnTeammates", 0),
                "totalMinionsKilled": participant.get("totalMinionsKilled", 0),
                "totalTimeCCDealt": participant.get("totalTimeCCDealt", 0),
                "totalTimeSpentDead": participant.get("totalTimeSpentDead", 0),
                "totalUnitsHealed": participant.get("totalUnitsHealed", 0),
                "tripleKills": participant.get("tripleKills", 0),
                "trueDamageDealt": participant.get("trueDamageDealt", 0),
                "trueDamageDealtToChampions": participant.get("trueDamageDealtToChampions", 0),
                "trueDamageTaken": participant.get("trueDamageTaken", 0),
                "turretKills": participant.get("turretKills", 0),
                "turretTakedowns": participant.get("turretTakedowns", 0),
                "turretsLost": participant.get("turretsLost", 0),
                "unrealKills": participant.get("unrealKills", 0),
                "visionScore": participant.get("visionScore", 0),
                "visionWardsBoughtInGame": participant.get("visionWardsBoughtInGame", 0),
                "wardsKilled": participant.get("wardsKilled", 0),
                "wardsPlaced": participant.get("wardsPlaced", 0),
                "win": participant.get("win", False)
            }
            all_players_info.append(player_info)

        return all_players_info

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
        action = AdminView().ask_choice()
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
            players = response.json()[:50]
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

    def get_game_datas(self, matchid):
        """
        Get data about a game from the database.

        Parameters
        ----------
        matchid : str
            The ID of the game to retrieve.

        Returns
        -------
        dict
            A dictionary containing game data.
        """
        try:
            query = """
                SELECT *
                FROM projet_info.games g
                WHERE g.matchid = %s
            """
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (matchid,))
                    res = cursor.fetchall()
            return res
        except Exception as e:
            print(f"Error getting game data for {matchid}: {e}")
            return {}

if __name__ == "__main__":
    print(DBGamesHandler().get_game_data("EUW1_6680437820"))