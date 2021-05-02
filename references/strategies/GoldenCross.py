import os, math
import sys
import pandas as pd
import backtrader as bt

class GoldenCross(bt.Strategy):
    params = (('fast', 50),
              ('slow', 100),
              ('order_pct', 0.95),
              ('ticker', 'SPY'))

    def __init__(self):
        self.fastma = bt.indicators.SMA(
            self.data.close, 
            period=self.p.fast, 
            plotname='20 day'
        )

        self.slowma = bt.indicators.SMA(
            self.data.close, 
            period=self.p.slow, 
            plotname='30 day'
        )

        self.sma_crossover = bt.indicators.CrossOver(
            self.fastma, 
            self.slowma
        )

    def set_sma(self, slow, fast):
        self.params['fast'] = fast
        self.params['slow'] = slow

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
        # print(f'sma crossover = {self.sma_crossover}')
        if self.position.size == 0:
            if self.sma_crossover > 0:
                amount_to_invest = (self.p.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.buy(size=self.size)
            
        if self.position.size > 0:
            if (self.sma_crossover < 0):
                print("Sell {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.sell(size=self.size)
                self.close()
