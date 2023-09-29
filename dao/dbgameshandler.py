from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from inputhandler.inputhandler import InputHandler
import requests
import os


class DBGamesHandler(metaclass=Singleton):

    params = {
        "api_key" : "RGAPI-bf396d46-13b8-437d-91a4-0193bc5e01c0"
    }
    
    @classmethod
    def update_database_games(cls, pseudo, start=0, count=60):
        player_puuid = DBGamesHandler.get_puuid(pseudo)
        last_games = DBGamesHandler.get_player_games(player_puuid, start, count)
        for game in last_games:
            if not DBGamesHandler.is_game_in_database(player_puuid, game):
                DBGamesHandler.add_game_information_to_database(player_puuid, game)


    @classmethod
    def get_puuid(cls, pseudo):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.players p "
                    f"where p.summonername = '{pseudo}'"
                )

                res = cursor.fetchone()
        if res:
            return res["puuid"]
        else:
            url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"
            response = requests.get(url, params=DBGamesHandler.params)
            return response.json()["puuid"]

    @classmethod
    def get_player_games(cls, puuid, start=0, count=100):
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        response = requests.get(url, params=DBGamesHandler.params)
        return response.json()

    @classmethod
    def is_game_in_database(cls, puuid, matchid):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT COUNT(*) as count
                    FROM projet_info.games g
                    WHERE g.puuid = %s AND g.matchid = %s
                """
                cursor.execute(query, (puuid, matchid))
                res = cursor.fetchone()["count"]
        return res == 1

    @classmethod
    def get_games_for_one_position(cls, puuid, poste):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT *
                    FROM projet_info.games g
                    WHERE g.puuid = %s AND g.poste = %s
                """
                cursor.execute(query, (puuid, poste))
                res = cursor.fetchall()
        return res    

    @classmethod
    def get_all_games_for_one_position(cls, poste):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * "
                    "FROM projet_info.games g "
                    f"WHERE g.poste = '{poste}'"
                )

                res = cursor.fetchall()
        return res       

    @classmethod
    def add_game_information_to_database(cls, puuid, matchid):
        infos = DBGamesHandler.get_all_variables_for_database(puuid, matchid)
        if infos["mapId"] == 11:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "insert into projet_info.games values('{puuid}', '{matchId}', '{poste}', '{resultat}', '{gameDuration}', '{kills}', '{assists}', '{deaths}', '{epicMonstersKilled}',\
                                                            '{totalMinionsKilled}', '{visionScore}', '{neutralMinionsKilled}', '{turretKills}', '{totalDamageDealtToChampions}',\
                                                            '{goldEarned}', '{wardsKilled}', '{wardsPlaced}', '{teamKills}', '{totalNeutralMinions}', '{totalEpicMonstersKilled}',\
                                                            '{teamNeutralMinionsKilled}')".format(**infos)
                    )

    @classmethod
    def get_all_variables_for_database(cls, puuid, matchid):
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchid}"
        response = requests.get(url, params=DBGamesHandler.params).json()

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

    @classmethod
    def get_player_id(cls, pseudo):
        url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"
        response = requests.get(url, params=DBGamesHandler.params).json()
        print(response)
        input()
        return response["id"]

    @classmethod
    def get_player_rank(cls, pseudo):
        id_player = DBGamesHandler.get_player_id(pseudo)
        print(id_player)
        input()
        url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id_player}"
        response = requests.get(url, params=DBGamesHandler.params).json()[0]
        return response["tier"]