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

    # def stop(self):
    #     # from settings import CONFIG
    #     from application.api.backtest.settings import CONFIG
    #     pnl = round(self.broker.getvalue() - CONFIG['capital_base'], 2)
    #     print('RSI Period: {} Final PnL: {}'.format(
    #         self.params.period, pnl))


def get_RSIStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    upper = strategy_params.get('upper') or 70
    lower = strategy_params.get('lower') or 30
    result = {
        'period': period,
        'upper': upper,
        'lower': lower
    }
    return result