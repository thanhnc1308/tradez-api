"""
Simple Moving Average
"""
import pandas as pd

def moving_average(df, length=200):
    """Calculate the moving average for the given data.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['Close'].rolling(length, min_periods=length).mean(), name='sma' + str(length))
    df = df.join(MA)
    return df
