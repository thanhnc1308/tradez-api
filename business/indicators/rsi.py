import statistics as stats
import pandas as pd


def calculate(df, time_period=20):
    """
    :param df: data
    :param time_period: look back period to compute gains & losses
    :return:
    """
    gain_history = []  # history of gains over look back period (0 if no gain, magnitude of gain if gain
    loss_history = []  # history of losses over look back period (0 if no loss, magnitude of loss if loss)
    avg_gain_values = []  # track avg gains for visualization purposes
    avg_loss_values = []  # track avg losses for visualization purposes
    rsi_values = []  # track computed RSI values
    last_price = 0  # current_price - last_price > 0 => gain. current_price - last_price < 0 => loss.
    close = df['Close']
    for close_price in close:
        if last_price == 0:
            last_price = close_price
        gain_history.append(max(0, close_price - last_price))
        loss_history.append(max(0, last_price - close_price))
        last_price = close_price
        # maximum observations is equal to lookback period
        if len(gain_history) > time_period:
            del (gain_history[0])
            del (loss_history[0])

        avg_gain = stats.mean(gain_history)
        avg_loss = stats.mean(loss_history)
        avg_gain_values.append(avg_gain)
        avg_loss_values.append(avg_loss)

        rs = 0
        if avg_loss > 0:  # to avoid division by 0, which is undefined
            rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
    df = df.assign(RSI_GAIN=pd.Series(avg_gain_values, index=df.index))
    df = df.assign(RSI_LOSS=pd.Series(avg_loss_values, index=df.index))
    df = df.assign(RSI=pd.Series(rsi_values, index=df.index))
    return df

