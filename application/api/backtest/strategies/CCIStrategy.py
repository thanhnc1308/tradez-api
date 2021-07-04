import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class CCIStrategy(BaseStrategy):

    params = (
        ('period', 14),
    )

    def __init__(self):
        self.cci = bt.indicators.CCI(self.data, period=self.params.period)
        super(CCIStrategy, self).__init__()

    def next(self):
        # print('self.cci', self.cci[0])
        super(CCIStrategy, self).next()

    def should_buy(self):
        return self.cci > 100

    def should_sell(self):
        return self.cci < -100


def get_CCIStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    result = {
        'period': period,
    }
    result = get_common_params(strategy_params, result)
    return result
