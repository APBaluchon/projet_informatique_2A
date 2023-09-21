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
    def get_player_games(cls, puuid):
        pass