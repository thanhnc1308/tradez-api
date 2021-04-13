import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy

class BollingerBandsSidewaytrategy(BaseStrategy):
    """This strategy uses Backtrader's BBand indicator and buys after the
    market dips into the lower band and sells on the moving average after the
    market hits the top band. This works great in sideways/bull markets.
    The idea is to buy during a low period and sell if the market dips below
    a moving average.
    """
    params = (
        ('period', 20),
        ('devfactor', 2),
    )

    def __init__(self):

        self.redline = None
        self.blueline = None

        # Add a BBand indicator
        self.bband = bt.indicators.BBands(self.datas[0],
                                          period=self.params.period,
                                          devfactor=self.params.devfactor)

        super(BollingerBandsSidewaytrategy, self).__init__()

    def next(self):
        super(BollingerBandsSidewaytrategy, self).next()

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if self.orefs:
            return

        if self.dataclose < self.bband.lines.bot and not self.position:
            self.redline = True

        if self.dataclose > self.bband.lines.top and self.position:
            self.blueline = True

        if self.dataclose > self.bband.lines.mid and not self.position and self.redline:
            self.buy()

        if self.dataclose < self.bband.lines.mid and self.position and self.blueline:
            self.sell()
            self.blueline = False
            self.redline = False

    def stop(self):
        from settings import CONFIG
        pnl = round(self.broker.getvalue() - CONFIG['capital_base'], 2)
        print('BollingerBandsSidewaytrategy Period: {} Final PnL: {}'.format(
            self.params.period, pnl))
