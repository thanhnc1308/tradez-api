import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class RSIStrategy(BaseStrategy):

    params = (
        ('period', 14),
        ('upper', 70),
        ('lower', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.period)
        super(RSIStrategy, self).__init__()

    def should_buy(self):
        return self.rsi < self.params.upper

    def should_sell(self):
        return self.rsi > self.params.lower


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
    result = get_common_params(strategy_params, result)
    return result
