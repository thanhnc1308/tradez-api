import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class BollingerBandsStrategy(BaseStrategy):
    """Bollinger Bands Strategy
    """

    params = (
        ('period', 20),
        ('devfactor', 2),
    )

    def __init__(self):
        # Add a BBand indicator
        self.bband = bt.indicators.BBands(self.datas[0],
                                          period=self.params.period,
                                          devfactor=self.params.devfactor)
        super(BollingerBandsStrategy, self).__init__()

    def next(self):
        super(BollingerBandsStrategy, self).next()

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if self.orefs:
            return

        if self.dataclose < self.bband.lines.bot and not self.position:
            self.buy()

        if self.dataclose > self.bband.lines.top and self.position:
            self.sell()

    def stop(self):
        from settings import CONFIG
        pnl = round(self.broker.getvalue() - CONFIG['capital_base'], 2)
        print('BollingerBandsStrategy Period: {} Final PnL: {}'.format(
            self.params.period, pnl))
