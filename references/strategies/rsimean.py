import os, math
import sys
import pandas as pd
import backtrader as bt


class RSIMean(bt.Strategy):
    params = (('rsi_period', 2),
              ('rsi_cross', 10),
              ('fast', 10),
              ('slow', 200),
              ('ticker', 'SPY'))

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(
            period=self.p.rsi_period,
            plotname='2 period rsi',
            safediv=True
        )
        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.fast,
            plotname='10 day'
        )

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.slow,
            plotname='200 day'
        )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

                gross_pnl = (order.executed.price - self.buyprice) * \
                            self.opsize

                net_pnl = gross_pnl - self.buycomm - order.executed.comm
                self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                     (gross_pnl, net_pnl))

    def next(self):
        if self.position.size == 0:
            if self.data.close[0] > self.slowma[0]:
                if self.rsi[0] < 10 and self.data.close[0] > self.fastma[0]:
                    print(f'self.data.close[0]:{self.data.close[0]} ')
                    print(f'self.slowma[0]: {self.slowma[0]:}')
                    print(f'self.rsi[0] : {self.rsi[0]}')
                    print(f'self.fastma[0]: {self.fastma[0]}')
                    print("Buy 1 shares of {} at {}".format(self.p.ticker,
                                                            self.data.close[0]))
                    self.buy(size=1)
        elif self.data.close[0] < self.fastma[0]:
            # if self.rsi[0] > 70:
            print(f'self.data.close: {self.data.close[0]}')
            print(f'self.fastma: {self.fastma[0]}')
            print("Sell 1 shares of {} at {}".format(self.p.ticker,
                                                      self.data.close[0]))
            self.sell(size=1)





        # if self.position.size == 0:
        #     if self.sma_crossover > 0:
        #         amount_to_invest = (self.p.order_pct * self.broker.cash)
        #         self.size = math.floor(amount_to_invest / self.data.close)
        #
        #         print("Buy {} shares of {} at {}".format(self.size, self.p.ticker,
        #                                                  self.data.close[0]))
        #         self.buy(size=self.size)
        #
        # if self.position.size > 0:
        #     if (self.sma_crossover < 0):
        #         print("Sell {} shares of {} at {}".format(self.size, self.p.ticker,
        #                                                   self.data.close[0]))
        #         self.close()
