from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from inputhandler.inputhandler import InputHandler
import requests
import os


class DBGamesHandler(metaclass=Singleton):

    params = {
        "api_key" : "RGAPI-497e6654-b07b-4f8e-8ede-662a10228b63"
    }

    @classmethod
    def generate_graph(cls):
        InputHandler.clear_screen()
        pseudo_to_analyze = InputHandler.get_input("Entrez le pseudo du joueur à analyser : ")
        DBGamesHandler.update_database(pseudo_to_analyze)
    
    @classmethod
    def update_database(cls, pseudo):
        player_puuid = DBGamesHandler.get_puuid(pseudo)
        last_games = DBGamesHandler.get_player_games(player_puuid, 0, 30)
        for game in last_games:
            if not DBGamesHandler.is_game_in_database(pseudo, game):
                DBGamesHandler.add_game_information_to_database(player_puuid, game)

    @classmethod
    def get_puuid(cls, pseudo):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet_info.utilisateur u "
                    f"where u.pseudo = '{pseudo}'"
                )

                res = cursor.fetchone()["puuid"]
        return res


    @classmethod
    def get_player_games(cls, puuid, start=0, count=100):
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        response = requests.get(url, params=DBGamesHandler.params)
        return response.json()

    @classmethod
    def is_game_in_database(cls, pseudo, matchid):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select count(*) from projet_info.games g "
                    f"where g.pseudo = '{pseudo}' and g.matchid = '{matchid}'"
                )

                res = cursor.fetchone()["count"]

        return res == 1

    @classmethod
    def add_game_information_to_database(cls, puuid, matchid):
        infos = DBGamesHandler.get_all_variables_for_database(puuid, matchid)
        if infos["mapId"] == 11:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "insert into projet_info.games values('{pseudo}', '{matchId}', '{poste}', '{gameDuration}', '{kills}', '{assists}', '{deaths}', '{epicMonstersKilled}',\
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
            "pseudo" : info_about_player["summonerName"],
            "matchId" : response["metadata"]["matchId"],
            "poste" : info_about_player["individualPosition"],
            "gameDuration" : response["info"]["gameDuration"],
            "kills" : info_about_player["kills"],
            "assists" : info_about_player["assists"],
            "deaths" : info_about_player["deaths"],
            "epicMonstersKilled" : info_about_player["dragonKills"]+info_about_player["baronKills"]+info_about_player["challenges"]["riftHeraldTakedowns"],
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
            infos_response["totalEpicMonstersKilled"] += participant["dragonKills"]+participant["baronKills"]+participant["challenges"]["riftHeraldTakedowns"]
            if participant["teamId"] == info_about_player["teamId"]:
                infos_response["teamNeutralMinionsKilled"] += participant["neutralMinionsKilled"]

        return infos_response

