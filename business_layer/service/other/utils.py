import pandas as pd
import numpy as np


class Utils:
    """
    A utility class with various helper methods.
    """
    def __init__(self):
        pass

    def interpolate(self, val, before_min, before_max):
        """
        Interpolate a value between two bounds.

        Parameters
        ----------
        val : float
            The value to interpolate.
        before_min : float
            The lower bound.
        before_max : float
            The upper bound.

        Returns
        -------
        float or None
            The interpolated value, or None if before_min equals before_max.
        """
        if before_min == before_max:
            return None
        
        if val <= before_min:
            return 0
        if val >= before_max:
            return 1

        proportion = (val - before_min) / (before_max - before_min)
        return proportion
    
    def convert_datas_to_dataframe(self, datas):
        """
        Convert a list of dictionaries to a pandas DataFrame.

        Parameters
        ----------
        datas : list of dict
            The list of dictionaries to convert.

        Returns
        -------
        pandas.DataFrame
            The resulting DataFrame.
        """
        df = pd.DataFrame(datas)
        df.drop(df[df['matchid'] == ''].index, inplace=True)
        df.loc['moyenne'] = df.select_dtypes(np.number).mean()
        df.loc['moyenne', df.select_dtypes('object').columns] = ''

        return df, df.iloc[-1]