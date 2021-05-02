
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('stoploss', 0.0005),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        #self.sma = bt.indicators.SimpleMovingAverage(
        #    self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        #bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        #bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                    subplot=True)
        #bt.indicators.StochasticSlow(self.datas[0])
        #bt.indicators.MACDHisto(self.datas[0])
        #rsi = bt.indicators.RSI(self.datas[0])
        #bt.indicators.SmoothedMovingAverage(rsi, period=10)
        #bt.indicators.ATR(self.datas[0], plot=False)

        # mine
        bb = bt.indicators.BollingerBands(self.datas[0])
        self.ema = bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        self.bb_low = bb.bot
        self.bb_mid = bb.mid

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.4f, Cost: %.4f, Comm %.4f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.4f, Cost: %.4f, Comm %.4f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))


            self.bar_executed = len(self)

            

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')


        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.4f, NET %.4f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.4f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        # if self.order:
        #     return

        # Check if we are in the market

        if self.position.size==0:

            # Not yet ... we MIGHT BUY if ...
            #if self.dataclose[0] > self.sma[0]:
            if (self.dataclose[0] < self.ema[0]) and (self.dataclose[0] < 1.0001 * self.bb_low[0]):

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.4f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

                stop_price = self.dataclose[0] * (1.0 - self.params.stoploss)
                self.stoploss_order = self.sell(exectype=bt.Order.Stop, price=stop_price)

            if self.dataclose[0] > self.bb_mid[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.4f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

                stop_price = self.dataclose[0] * (1.0 + self.params.stoploss)
                self.stoploss_order = self.buy(exectype=bt.Order.Stop, price=stop_price)

        elif self.position.size>0:
 
            if self.dataclose[0] > self.bb_mid[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.4f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                self.cancel(self.stoploss_order)

        elif self.position.size<0:

            if (self.dataclose[0] < self.ema[0]) and (self.dataclose[0] < 1.0001 * self.bb_low[0]):

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.4f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
                self.cancel(self.stoploss_order)


def backtest(pair):
    # Create a cerebro entity
    cerebro = bt.Cerebro(cheat_on_open=True)

    cerebro.addobserver(bt.observers.DrawDown)

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # cerebro.addobserver(bt.observers.BuySell)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, 'backtrader/datas/orcl-1995-2014.txt')
    datapath = os.path.join(modpath, pair)
    # print(datapath)

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(dataname=datapath, dtformat=('%Y-%m-%d %H:%M:%S'), openinterest=-1, timeframe=bt.TimeFrame.Minutes, compression=5, fromdate=datetime(2020, 6, 14), todate=datetime(2020, 9, 14))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(50000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.SizerFix, stake=1000)

    # Set the commission
    cerebro.broker.setcommission(commission=0.00001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.4f' % cerebro.broker.getvalue())

    # Analyzer
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe', timeframe=bt.TimeFrame.Weeks)
    # cerebro.addanalyzer(bt.analyzers.Calmar, _name='mycalmar', timeframe=bt.TimeFrame.Months)
    # cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio', timeframe=bt.TimeFrame.Minutes, compression=5)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='mydrawdown')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='mysqn')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='mytradeanalyzer')
    cerebro.addanalyzer(bt.analyzers.VWR, _name='myvwr')

    # Run over everything
    thestrats = cerebro.run()
    thestrat = thestrats[0]

    print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis()['sharperatio'])
    # print('Calmar Ratio:', thestrat.analyzers.mycalmar.get_analysis())
    print('MaxDrawDown:', (thestrat.analyzers.mydrawdown.get_analysis().max.drawdown)*100, "%")
    print('MaxDrawDown Time (min):', (thestrat.analyzers.mydrawdown.get_analysis().max.len)/60)
    '''
    SQN
    1.6 - 1.9 Below average
    2.0 - 2.4 Average
    2.5 - 2.9 Good
    3.0 - 5.0 Excellent
    5.1 - 6.9 Superb
    7.0 - Holy Grail?
    '''
    print('SQN:', thestrat.analyzers.mysqn.get_analysis())
    print('TradeAnalyzer:', thestrat.analyzers.mytradeanalyzer.get_analysis())
    print('VWR:', thestrat.analyzers.myvwr.get_analysis()['vwr'])

    # pyfoliozer = thestrat.analyzers.getbyname('pyfolio')
    # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    # import pyfolio as pf
    # pf.create_full_tear_sheet(
    #     returns,
    #     positions=positions,
    #     transactions=transactions,
    #     gross_lev=gross_lev,
    #     live_start_date='2020-06-14',  # This date is sample specific
    #     round_trips=True)

    # Print out the final result
    print('Final Portfolio Value: %.4f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot(volume=False)



if __name__ == '__main__':
    # Be careful of value of pair 
    pair_list = ['OANDA:AUD_USD:5.csv', 'OANDA:EUR_JPY:5.csv', 'OANDA:EUR_USD:5.csv', 'OANDA:GBP_USD:5.csv', 'OANDA:USD_JPY:5.csv']
    # pair_list = ['OANDA:AUD_USD:1.csv', 'OANDA:EUR_JPY:1.csv', 'OANDA:EUR_USD:1.csv', 'OANDA:GBP_USD:1.csv', 'OANDA:USD_JPY:1.csv']

    for pair in pair_list:
        backtest(pair)