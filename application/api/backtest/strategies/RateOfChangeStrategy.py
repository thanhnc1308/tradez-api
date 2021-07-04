import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class RateOfChangeStrategy(BaseStrategy):

    params = (
        ('period', 9),
    )

    def __init__(self):
        self.roc = bt.indicators.RateOfChange(self.data.close, period=self.params.period)
        super(RateOfChangeStrategy, self).__init__()

    def next(self):
        print('self.roc[0]', self.roc[0])
        # print('self.roc[1]', self.roc[1])
        print('self.roc[-1]', self.roc[-1])
        super(RateOfChangeStrategy, self).next()

    def should_buy(self):
        return self.roc[0] > 0 and self.roc[-1] < 0

    def should_sell(self):
        return self.roc[0] < 0 and self.roc[-1] > 0


def get_RateOfChangeStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 9
    result = {
        'period': period,
    }
    result = get_common_params(strategy_params, result)
    return result
