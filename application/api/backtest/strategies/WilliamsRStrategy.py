import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class WilliamsRStrategy(BaseStrategy):

    params = (
        ('period', 14),
        ('upper', -20),
        ('lower', -80),
    )

    def __init__(self):
        self.william_percent_r = bt.indicators.WilliamsR(self.data, period=self.params.period)
        super(WilliamsRStrategy, self).__init__()

    def should_buy(self):
        return self.william_percent_r < self.params.upper

    def should_sell(self):
        return self.william_percent_r > self.params.lower


def get_WilliamsRStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    upper = strategy_params.get('upper') or -20
    lower = strategy_params.get('lower') or -80
    result = {
        'period': period,
        'upper': upper,
        'lower': lower
    }
    result = get_common_params(strategy_params, result)
    return result
