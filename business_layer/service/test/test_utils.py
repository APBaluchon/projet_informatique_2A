import unittest
from business_layer.service.other.utils import Utils
import pandas as pd


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()

    def test_interpolate(self):
        self.assertEqual(self.utils.interpolate(5, 0, 10), 0.5)
        self.assertEqual(self.utils.interpolate(10, 0, 10), 1)
        self.assertEqual(self.utils.interpolate(0, 0, 10), 0)
        self.assertEqual(self.utils.interpolate(15, 0, 10), 1)

    def test_convert_datas_to_dataframe(self):
        datas = [
            {'name': 'John', 'age': 25},
            {'name': 'Jane', 'age': 30},
            {'name': 'Bob', 'age': 35}
        ]
        expected_df = pd.DataFrame(datas)
        df = self.utils.convert_datas_to_dataframe(datas)[0]
        self.assertTrue(df.equals(expected_df))


if __name__ == '__main__':
    unittest.main()
