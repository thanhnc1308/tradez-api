import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class RSIStrategy2(bt.SignalStrategy):
    def __init__(self):
        self.index = bt.ind.RelativeStrengthIndex()

    def next(self):
        if self.index < 40 and self.datas[0].close[0] > self.datas[-1].close[-1]:
            self.buy(size=0.5)

        elif self.index > 70 and self.datas[0].close[0] < self.datas[-1].close[-1]:
            self.close(size=0.5)

        if self.datas[0].datetime.date(0) == datetime(2020, 1, 29).date():
            self.close()