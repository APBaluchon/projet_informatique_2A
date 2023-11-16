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
        "api_key" : "RGAPI-fce0bb0b-71ec-4b72-b1a1-c99ec7c8d038"
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
        if infos["queueId"] in [420, 440]:
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
                            infos["matchId"], infos["puuid"], infos["assists"], infos["baronKills"], infos["bountyLevel"], 
                            infos["champExperience"], infos["champLevel"], infos["championName"], infos["consumablesPurchased"], 
                            infos["damageDealtToBuildings"], infos["damageDealtToObjectives"], infos["damageDealtToTurrets"], 
                            infos["damageSelfMitigated"], infos["deaths"], infos["detectorWardsPlaced"], infos["doubleKills"], 
                            infos["dragonKills"], infos["firstBloodAssist"], infos["firstBloodKill"], infos["firstTowerAssist"], 
                            infos["firstTowerKill"], infos["gameDuration"], infos["gameEndedInEarlySurrender"], infos["gameEndedInSurrender"], 
                            infos["goldEarned"], infos["goldSpent"], infos["inhibitorKills"], infos["inhibitorTakedowns"], 
                            infos["inhibitorsLost"], infos["item0"], infos["item1"], infos["item2"], infos["item3"], infos["item4"], infos["item5"], 
                            infos["item6"], infos["itemsPurchased"], infos["killingSprees"], infos["kills"], 
                            infos["largestCriticalStrike"], infos["largestKillingSpree"], infos["largestMultiKill"], 
                            infos["longestTimeSpentLiving"], infos["magicDamageDealt"], infos["magicDamageDealtToChampions"], 
                            infos["magicDamageTaken"], infos["neutralMinionsKilled"], infos["nexusKills"], infos["nexusTakedowns"], 
                            infos["nexusLost"], infos["objectivesStolen"], infos["objectivesStolenAssists"], infos["participantId"], 
                            infos["pentaKills"], infos["physicalDamageDealt"], infos["physicalDamageDealtToChampions"], 
                            infos["physicalDamageTaken"], infos["quadraKills"], infos["riotIdName"], 
                            infos["riotIdTagline"], infos["sightWardsBoughtInGame"], infos["spell1Casts"], 
                            infos["spell2Casts"], infos["spell3Casts"], infos["spell4Casts"], infos["summoner1Casts"], 
                            infos["summoner1Id"], infos["summoner2Casts"], infos["summoner2Id"], infos["teamEarlySurrendered"], infos["teamId"], 
                            infos["teamKills"], infos["teamPosition"], infos["timeCCingOthers"], infos["timePlayed"], infos["totalDamageDealt"], 
                            infos["totalDamageDealtToChampions"], infos["totalDamageShieldedOnTeammates"], 
                            infos["totalDamageTaken"], infos["totalHeal"], infos["totalHealsOnTeammates"], infos["totalMinionsKilled"], 
                            infos["totalTimeCCDealt"], infos["totalTimeSpentDead"], infos["totalUnitsHealed"], infos["tripleKills"], 
                            infos["trueDamageDealt"], infos["trueDamageDealtToChampions"], infos["trueDamageTaken"], 
                            infos["turretKills"], infos["turretTakedowns"], infos["turretsLost"], infos["unrealKills"], infos["visionScore"], 
                            infos["visionWardsBoughtInGame"], infos["wardsKilled"], infos["wardsPlaced"], infos["win"]
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

        info_about_player = None
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                info_about_player = participant
                break

        infos_response = {
            "queueId": response["info"]["queueId"],
            "mapId": response["info"]["mapId"],
            "matchId": response["metadata"]["matchId"],
            "puuid": info_about_player.get("puuid", ""),
            "assists": info_about_player.get("assists", 0),
            "baronKills": info_about_player.get("baronKills", 0),
            "bountyLevel": info_about_player.get("bountyLevel", 0),
            "champExperience": info_about_player.get("champExperience", 0),
            "champLevel": info_about_player.get("champLevel", 0),
            "championName": info_about_player.get("championName", ""),
            "consumablesPurchased": info_about_player.get("consumablesPurchased", 0),
            "damageDealtToBuildings": info_about_player.get("damageDealtToBuildings", 0),
            "damageDealtToObjectives": info_about_player.get("damageDealtToObjectives", 0),
            "damageDealtToTurrets": info_about_player.get("damageDealtToTurrets", 0),
            "damageSelfMitigated": info_about_player.get("damageSelfMitigated", 0),
            "deaths": info_about_player.get("deaths", 0),
            "detectorWardsPlaced": info_about_player.get("detectorWardsPlaced", 0),
            "doubleKills": info_about_player.get("doubleKills", 0),
            "dragonKills": info_about_player.get("dragonKills", 0),
            "firstBloodAssist": info_about_player.get("firstBloodAssist", False),
            "firstBloodKill": info_about_player.get("firstBloodKill", False),
            "firstTowerAssist": info_about_player.get("firstTowerAssist", False),
            "firstTowerKill": info_about_player.get("firstTowerKill", False),
            "gameDuration": response["info"]["gameDuration"],
            "gameEndedInEarlySurrender": info_about_player.get("gameEndedInEarlySurrender", False),
            "gameEndedInSurrender": info_about_player.get("gameEndedInSurrender", False),
            "goldEarned": info_about_player.get("goldEarned", 0),
            "goldSpent": info_about_player.get("goldSpent", 0),
            "inhibitorKills": info_about_player.get("inhibitorKills", 0),
            "inhibitorTakedowns": info_about_player.get("inhibitorTakedowns", 0),
            "inhibitorsLost": info_about_player.get("inhibitorsLost", 0),
            "item0": info_about_player.get("item0", 0),
            "item1": info_about_player.get("item1", 0),
            "item2": info_about_player.get("item2", 0),
            "item3": info_about_player.get("item3", 0),
            "item4": info_about_player.get("item4", 0),
            "item5": info_about_player.get("item5", 0),
            "item6": info_about_player.get("item6", 0),
            "itemsPurchased": info_about_player.get("itemsPurchased", 0),
            "killingSprees": info_about_player.get("killingSprees", 0),
            "kills": info_about_player.get("kills", 0),
            "largestCriticalStrike": info_about_player.get("largestCriticalStrike", 0),
            "largestKillingSpree": info_about_player.get("largestKillingSpree", 0),
            "largestMultiKill": info_about_player.get("largestMultiKill", 0),
            "longestTimeSpentLiving": info_about_player.get("longestTimeSpentLiving", 0),
            "magicDamageDealt": info_about_player.get("magicDamageDealt", 0),
            "magicDamageDealtToChampions": info_about_player.get("magicDamageDealtToChampions", 0),
            "magicDamageTaken": info_about_player.get("magicDamageTaken", 0),
            "neutralMinionsKilled": info_about_player.get("neutralMinionsKilled", 0),
            "nexusKills": info_about_player.get("nexusKills", 0),
            "nexusTakedowns": info_about_player.get("nexusTakedowns", 0),
            "nexusLost": info_about_player.get("nexusLost", 0),
            "objectivesStolen": info_about_player.get("objectivesStolen", 0),
            "objectivesStolenAssists": info_about_player.get("objectivesStolenAssists", 0),
            "participantId": info_about_player.get("participantId", 0),
            "pentaKills": info_about_player.get("pentaKills", 0),
            "physicalDamageDealt": info_about_player.get("physicalDamageDealt", 0),
            "physicalDamageDealtToChampions": info_about_player.get("physicalDamageDealtToChampions", 0),
            "physicalDamageTaken": info_about_player.get("physicalDamageTaken", 0),
            "quadraKills": info_about_player.get("quadraKills", 0),
            "riotIdName": info_about_player.get("riotIdName", ""),
            "riotIdTagline": info_about_player.get("riotIdTagline", ""),
            "sightWardsBoughtInGame": info_about_player.get("sightWardsBoughtInGame", 0),
            "spell1Casts": info_about_player.get("spell1Casts", 0),
            "spell2Casts": info_about_player.get("spell2Casts", 0),
            "spell3Casts": info_about_player.get("spell3Casts", 0),
            "spell4Casts": info_about_player.get("spell4Casts", 0),
            "summoner1Casts": info_about_player.get("summoner1Casts", 0),
            "summoner1Id": info_about_player.get("summoner1Id", 0),
            "summoner2Casts": info_about_player.get("summoner2Casts", 0),
            "summoner2Id": info_about_player.get("summoner2Id", 0),
            "teamEarlySurrendered": info_about_player.get("teamEarlySurrendered", False),
            "teamId": info_about_player.get("teamId", 0),
            "teamKills": sum([p["kills"] for p in response["info"]["participants"]]),
            "teamPosition": info_about_player.get("teamPosition", ""),
            "timeCCingOthers": info_about_player.get("timeCCingOthers", 0),
            "timePlayed": info_about_player.get("timePlayed", 0),
            "totalDamageDealt": info_about_player.get("totalDamageDealt", 0),
            "totalDamageDealtToChampions": info_about_player.get("totalDamageDealtToChampions", 0),
            "totalDamageShieldedOnTeammates": info_about_player.get("totalDamageShieldedOnTeammates", 0),
            "totalDamageTaken": info_about_player.get("totalDamageTaken", 0),
            "totalHeal": info_about_player.get("totalHeal", 0),
            "totalHealsOnTeammates": info_about_player.get("totalHealsOnTeammates", 0),
            "totalMinionsKilled": info_about_player.get("totalMinionsKilled", 0),
            "totalTimeCCDealt": info_about_player.get("totalTimeCCDealt", 0),
            "totalTimeSpentDead": info_about_player.get("totalTimeSpentDead", 0),
            "totalUnitsHealed": info_about_player.get("totalUnitsHealed", 0),
            "tripleKills": info_about_player.get("tripleKills", 0),
            "trueDamageDealt": info_about_player.get("trueDamageDealt", 0),
            "trueDamageDealtToChampions": info_about_player.get("trueDamageDealtToChampions", 0),
            "trueDamageTaken": info_about_player.get("trueDamageTaken", 0),
            "turretKills": info_about_player.get("turretKills", 0),
            "turretTakedowns": info_about_player.get("turretTakedowns", 0),
            "turretsLost": info_about_player.get("turretsLost", 0),
            "unrealKills": info_about_player.get("unrealKills", 0),
            "visionScore": info_about_player.get("visionScore", 0),
            "visionWardsBoughtInGame": info_about_player.get("visionWardsBoughtInGame", 0),
            "wardsKilled": info_about_player.get("wardsKilled", 0),
            "wardsPlaced": info_about_player.get("wardsPlaced", 0),
            "win": info_about_player.get("win", False)
        }

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