import unittest
from business_layer.service.game.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        game_data = {
            "assists": 5,
            "championname": "Ahri",
            "deaths": 3,
            "damagedealttoturrets": 2000,
            "gameduration": 1800,
            "kills": 10,
            "matchid": "123456789",
            "puuid": "abcdefg123456",
            "spell1casts": 20,
            "spell2casts": 15,
            "spell3casts": 12,
            "spell4casts": 8,
            "timeccingothers": 30,
            "totaldamagedealttochampions": 15000,
            "totaldamagetaken": 10000,
            "totalhealsonteammates": 5,
            "totalminionskilled": 200,
            "totaldamageshieldedonteammates": 5000,
            "turretkills": 2,
            "wardsplaced": 10,
            "win": True
        }
        self.game = Game(game_data)

    def test_get_assists(self):
        self.assertEqual(self.game.get_assists(), 5)

    def test_get_championname(self):
        self.assertEqual(self.game.get_championname(), "Ahri")

    def test_get_deaths(self):
        self.assertEqual(self.game.get_deaths(), 3)

    def test_get_damagedealttoturrets(self):
        self.assertEqual(self.game.get_damagedealttoturrets(), 2000)

    def test_get_gameduration(self):
        self.assertEqual(self.game.get_gameduration(), 1800)

    def test_get_kills(self):
        self.assertEqual(self.game.get_kills(), 10)

    def test_get_matchid(self):
        self.assertEqual(self.game.get_matchid(), "123456789")

    def test_get_puuid(self):
        self.assertEqual(self.game.get_puuid(), "abcdefg123456")

    def test_get_totaldamagedealttochampions(self):
        self.assertEqual(self.game.get_totaldamagedealttochampions(), 15000)

    def test_get_totaldamagetaken(self):
        self.assertEqual(self.game.get_totaldamagetaken(), 10000)

    def test_get_totalminionskilled(self):
        self.assertEqual(self.game.get_totalminionskilled(), 200)

    def test_get_turretkills(self):
        self.assertEqual(self.game.get_turretkills(), 2)

    def test_get_wardsplaced(self):
        self.assertEqual(self.game.get_wardsplaced(), 10)

    def test_get_win(self):
        self.assertEqual(self.game.get_win(), True)


if __name__ == "__main__":
    unittest.main()