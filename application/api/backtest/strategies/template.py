import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class StrategyTemplate(BaseStrategy):
    params = ()

    def __init__(self):
        super(StrategyTemplate, self).__init__()

    def next(self):

        if True:
            pass
            # self.buy()
        else:
            pass
            # self.sell()
