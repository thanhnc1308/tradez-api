import matplotlib.pyplot as plt


def draw_ema(df):
    """
    function draw ema
    :param df:
    :return:
    """
    close_price = df['Close']
    ema = df['ema']
    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Market price in $')
    close_price.plot(ax=ax1, color='g', lw=2., legend=True)
    ema.plot(ax=ax1, color='b', lw=2., legend=True)
    plt.show()


def draw_rsi(df):
    close_price = df['Close']
    rs_gain = df['RSI_GAIN']
    rs_loss = df['RSI_LOSS']
    rsi = df['RSI']

    fig = plt.figure()
    ax1 = fig.add_subplot(311, ylabel='Market price in $')
    close_price.plot(ax=ax1, color='black', lw=2., legend=True)
    ax2 = fig.add_subplot(312, ylabel='RS')
    rs_gain.plot(ax=ax2, color='g', lw=2., legend=True)
    rs_loss.plot(ax=ax2, color='r', lw=2., legend=True)
    ax3 = fig.add_subplot(313, ylabel='RSI')
    rsi.plot(ax=ax3, color='b', lw=2., legend=True)
    plt.show()
