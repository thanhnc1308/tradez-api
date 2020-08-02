import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculate(df, num_periods=20):
    smooth_coefficient = 2 / (num_periods + 1)  # smoothing constant
    ema_p = 0
    ema_values = []  # to hold computed EMA values
    close = df['Close']
    for close_price in close:
        if ema_p == 0:  # first observation, EMA = current-price
            ema_p = close_price
        else:
            ema_p = (close_price - ema_p) * smooth_coefficient + ema_p
        ema_values.append(ema_p)
    df = df.assign(ema=pd.Series(ema_values, index=df.index))
    return df


def double_moving_average(df, short_ma=20, long_ma=100):
    """
    :param df:
    :param short_ma:
    :param long_ma:
    :return: signals - True if the short-term moving average is higher than the long-term moving average
            orders - 1 for the buy order, and -1 for the sell order
    """
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0
    signals['short_ma'] = df['Close'].rolling(window=short_ma, min_periods=1, center=False).mean()
    signals['long_ma'] = df['Close'].rolling(window=long_ma, min_periods=1, center=False).mean()
    signals['signal'][short_ma:] = np.where(signals['short_ma'][short_ma:] > signals['long_ma'][short_ma:], 1.0, 0.0)
    signals['orders'] = signals['signal'].diff()
    return signals


def draw_dual_ma(df):
    """
    df must have short_ma, long_ma, orders columns
    :param df:
    :return:
    """
    ts = double_moving_average(df)
    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Google price in $')
    df["Close"].plot(ax=ax1, color='g', lw=.5)
    ts["short_ma"].plot(ax=ax1, color='r', lw=2.)
    ts["long_ma"].plot(ax=ax1, color='b', lw=2.)
    ax1.plot(ts.loc[ts.orders == 1.0].index, df["Close"][ts.orders == 1.0], '^', markersize=7, color='k')
    ax1.plot(ts.loc[ts.orders == -1.0].index, df["Close"][ts.orders == -1.0], 'v', markersize=7, color='k')
    plt.legend(["Price", "Short mavg", "Long mavg", "Buy", "Sell"])
    plt.title("Double Moving Average Trading Strategy")
    plt.show()
