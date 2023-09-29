from dao.dbconnection import DBConnection
from singleton.singleton import Singleton
from inputhandler.inputhandler import InputHandler
import requests
import os
from dao.dbgameshandler import DBGamesHandler


class DBPlayersHandler(metaclass=Singleton):

    @classmethod
    def update_database_players(cls, pseudo):
        res = 1
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select count(*) as count from projet_info.players p "
                    f"where p.summonername = '{pseudo}'"
                )

                res = cursor.fetchone()["count"]

        if res == 0:
            rank = DBGamesHandler.get_player_rank(pseudo)
            puuid = DBGamesHandler.get_puuid(pseudo)
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                            f"insert into projet_info.players values('{puuid}', '{pseudo}', '{rank}')"
                    )
