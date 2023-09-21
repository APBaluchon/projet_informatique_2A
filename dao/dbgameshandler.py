from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from inputhandler.inputhandler import InputHandler
import requests
import os


class DBGamesHandler(metaclass=Singleton):

    params = {
        "api_key" : "RGAPI-56478d67-2567-4881-98d4-17d3875ba4d8"
    }
    
    @classmethod
    def update_database(cls, pseudo):
        player_puuid = DBGamesHandler.get_puuid(pseudo)
        last_games = DBGamesHandler.get_player_games(player_puuid)
        for game in last_games:
            if not DBGamesHandler.is_game_in_database(pseudo, game):
                pass

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
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/RG-9GlIyT5ZLGjQebAyjP-ejq59OI4O9cfGwyt2M9q1nOJ8WLFkBMnZWww66Vt6XrURnVXuiDiT9Qg/ids?start={start}&count={count}"
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
    def add_game_information_to_database(cls, pseudo, matchid):
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{matchid}"
        response = requests.get(url, params=DBGamesHandler.params).json()