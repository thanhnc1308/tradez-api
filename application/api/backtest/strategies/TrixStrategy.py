import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class TrixStrategy(BaseStrategy):

    params = (
        ('period', 18),
    )

    def __init__(self):
        self.trix = bt.indicators.Trix(self.data.close, period=self.params.period)
        super(TrixStrategy, self).__init__()

    def next(self):
        print('self.trix[0]', self.trix[0])
        # print('self.trix[1]', self.trix[1])
        print('self.trix[-1]', self.trix[-1])
        super(TrixStrategy, self).next()

    def should_buy(self):
        return self.trix[0] > 0 and self.trix[-1] < 0

    def should_sell(self):
        return self.trix[0] < 0 and self.trix[-1] > 0


def get_TrixStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 18
    result = {
        'period': period,
    }
    result = get_common_params(strategy_params, result)
    return result
