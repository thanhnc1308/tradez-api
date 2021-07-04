import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class VortexStrategy(BaseStrategy):

    params = (
        ('period', 14),
    )

    def __init__(self):
        self.vortex = bt.indicators.Vortex(self.data, period=self.params.period)
        super(VortexStrategy, self).__init__()

    def next(self):
        print('self.vortex.lines.vi_plus[0]', self.vortex.lines.vi_plus[0])
        print('self.vortex.lines.vi_plus[-1]', self.vortex.lines.vi_plus[-1])
        print('self.vortex.lines.vi_minus[0]', self.vortex.lines.vi_minus[0])
        print('self.vortex.lines.vi_minus[-1]', self.vortex.lines.vi_minus[-1])
        super(VortexStrategy, self).next()

    def should_buy(self):
        return self.vortex.lines.vi_plus[0] > self.vortex.lines.vi_minus[0] and self.vortex.lines.vi_plus[-1] < self.vortex.lines.vi_minus[-1]

    def should_sell(self):
        return self.vortex.lines.vi_plus[0] < self.vortex.lines.vi_minus[0] and self.vortex.lines.vi_plus[-1] > self.vortex.lines.vi_minus[-1]


def get_VortexStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    result = {
        'period': period,
    }
    result = get_common_params(strategy_params, result)
    return result
