import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class EnvelopeStrategy(BaseStrategy):

    params = (
        ('perc', 10),
    )

    def __init__(self):
        self.envelope = bt.indicators.Envelope(self.data.close, perc=self.params.perc)
        super(EnvelopeStrategy, self).__init__()

    def next(self):
        # print('self.envelope[0]', self.envelope[0])
        super(EnvelopeStrategy, self).next()

    def should_buy(self):
        return self.envelope.lines.bot[0] > self.envelope.lines.src[0]

    def should_sell(self):
        return self.envelope.lines.top[0] < self.envelope.lines.src[0]


def get_EnvelopeStrategy_params(config):
    strategy_params = config.get('strategy_params')
    perc = strategy_params.get('perc') or 10
    result = {
        'perc': perc,
    }
    result = get_common_params(strategy_params, result)
    return result
