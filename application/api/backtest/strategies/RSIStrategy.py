import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class RSIStrategy(BaseStrategy):

    params = (
        ('period', 14),
        ('upper', 70),
        ('lower', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close,
                                         period=self.params.period)
        super(RSIStrategy, self).__init__()

    def next(self):
        if not self.position:
            if self.rsi < self.params.upper:
                self.buy()
        else:
            if self.rsi > self.params.lower:
                self.sell()

    def stop(self):
        # from settings import CONFIG
        from application.api.backtest.settings import CONFIG
        pnl = round(self.broker.getvalue() - CONFIG['capital_base'], 2)
        print('RSI Period: {} Final PnL: {}'.format(
            self.params.period, pnl))
