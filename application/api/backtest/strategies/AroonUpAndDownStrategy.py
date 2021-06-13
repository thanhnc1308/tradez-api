import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class AroonUpAndDownStrategy(BaseStrategy):

    params = (
        ('period', 14),
    )

    def __init__(self):
        self.aroon = bt.indicators.AroonUpDownOscillator(self.data, period=self.params.period)
        self.prev_aroon_osc = 0
        super(AroonUpAndDownStrategy, self).__init__()

    def next(self):
        print('self.aroon.lines.aroonup', self.aroon.lines.aroonup)
        print('self.aroon.lines.aroondown', self.aroon.lines.aroondown)
        print('self.aroon.lines.aroonosc', self.aroon.lines.aroonosc)
        super(AroonUpAndDownStrategy, self).next()

    def should_buy(self):
        return False

    def should_sell(self):
        return False


def get_AroonUpAndDownStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    result = {
        'period': period,
    }
    result = get_common_params(strategy_params, result)
    return result
