import unittest
from business_layer.dao.dbhandler import DBHandler


class TestDBHandler(unittest.TestCase):

    def setUp(self):
        self.db_handler = DBHandler()

    def test_get_user_role(self):
        result = self.db_handler.get_user_role("admin")
        self.assertEqual(result, "admin")

        result = self.db_handler.get_user_role("SlolyS")
        self.assertEqual(result, "user")

        result = self.db_handler.get_user_role("pimpon")
        self.assertIsNone(result)

    def test_is_user_in_db(self):
        result = self.db_handler.is_user_in_db("SlolyS")
        self.assertTrue(result)

        result = self.db_handler.is_user_in_db("pimpon")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()