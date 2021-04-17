import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class MACD(bt.Strategy):
    params = (
        ("macd1", 12),
        ("macd2", 26),
        ("macdsig", 9),
        # Percentage of portfolio for a trade. Something is left for the fees
        # otherwise orders would be rejected
        ("portfolio_frac", 0.98),
    )

    def __init__(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash
        self.size = None
        self.order = None

        self.macd = bt.ind.MACD(
            self.data,
            period_me1=self.p.macd1,
            period_me2=self.p.macd2,
            period_signal=self.p.macdsig,
        )
        # Cross of macd and macd signal
        self.mcross = bt.ind.CrossOver(self.macd.macd, self.macd.signal)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.order=None
        print('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        print(
            f"DateTime {self.datas[0].datetime.datetime(0)}, "
            f"Price {self.data[0]:.2f}, Mcross {self.mcross[0]}, "
            f"Position {self.position.upopened}"
        )
        if not self.order:  # not in the market
            if self.mcross[0] > 0.0:
                print("Starting buy order")
                self.size = (self.broker.get_cash() / self.datas[0].close * self.p.portfolio_frac)
                self.order = self.buy(size=self.size)
                #self.order=self.buy()
        else:  # in the market
            if self.mcross[0] < 0.0:
                print("Starting sell order")
                self.order = self.sell(size=self.size)