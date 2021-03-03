"""
Relative Vigor Index
"""
import pandas as pd


def calculate(df, length=14, source='close'):
    """
    :param source: Open Close High Low
    :param df: data
    :param length: look back period to compute gains & losses
    :return:
    """
    df = df.assign(RSI=pd.Series([], index=df.index))
    return df
