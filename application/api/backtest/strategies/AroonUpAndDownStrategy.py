import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class AroonUpAndDownStrategy(BaseStrategy):

    params = (
        ('period', 14),
    )

    def __init__(self):
        self.aroon = bt.indicators.AroonUpDownOscillator(self.data, period=self.params.period)
        self.is_aroon_up_above_aroon_down = True
        super(AroonUpAndDownStrategy, self).__init__()

    def next(self):
        # print('date: ', self.datas[0].datetime.date(0))
        # print('self.aroon.lines.aroonup', self.aroon.lines.aroonup[0])
        # print('self.aroon.lines.aroondown', self.aroon.lines.aroondown[0])
        # print('self.aroon.lines.aroonosc', self.aroon.lines.aroonosc[0])
        super(AroonUpAndDownStrategy, self).next()
        if self.aroon.lines.aroonup[0] > self.aroon.lines.aroondown[0]:
            self.is_aroon_up_above_aroon_down = True
        else:
            self.is_aroon_up_above_aroon_down = False

    def should_sell(self):
        return not self.is_aroon_up_above_aroon_down and self.aroon.lines.aroonup[0] > self.aroon.lines.aroondown[0]

    def should_buy(self):
        return self.is_aroon_up_above_aroon_down and self.aroon.lines.aroonup[0] < self.aroon.lines.aroondown[0]


def get_AroonUpAndDownStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    result = {
        'period': period,
    }
    result = get_common_params(strategy_params, result)
    return result
