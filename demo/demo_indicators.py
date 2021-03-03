"""This is a example adding bollinger band features.
"""
import pandas as pd
import ta

# Load data
df = pd.read_csv("../test/data/datas.csv", sep=",")

# Clean nan values
df = ta.utils.dropna(df)

print(df.columns)

# Add bollinger band high indicator filling nans values
df["bb_high_indicator"] = ta.volatility.bollinger_hband_indicator(
    df["Close"], window=20, window_dev=2, fillna=True
)

# Add bollinger band low indicator filling nans values
df["bb_low_indicator"] = ta.volatility.bollinger_lband_indicator(
    df["Close"], window=20, window_dev=2, fillna=True
)

print(df.columns)


# # Load data
# df = pd.read_csv("../test/data/datas.csv", sep=",")

# # Clean nan values
# df = ta.utils.dropna(df)

# window = 12
# df[f"roc_{window}"] = ta.momentum.ROCIndicator(close=df["Close"], window=window).roc()



# Load data
# df = pd.read_csv("../test/data/datas.csv", sep=",")

# # Clean nan values
# df = ta.utils.dropna(df)

# print(df.columns)

# # Add all volume features filling nans values
# df = ta.add_volume_ta(df, "High", "Low", "Close", "Volume_BTC", fillna=True)

# print(df.columns)


# df[f"{colprefix}volume_obv"] = OnBalanceVolumeIndicator(
#         close=df[close], volume=df[volume], fillna=fillna
#     ).on_balance_volume()


# # Money Flow Indicator
# df[f"{colprefix}volume_mfi"] = MFIIndicator(
#     high=df[high],
#     low=df[low],
#     close=df[close],
#     volume=df[volume],
#     window=14,
#     fillna=fillna,
# ).money_flow_index()