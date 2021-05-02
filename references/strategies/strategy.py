# import datetime  # For datetime objects
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

# Create a Strategy
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED: {order.executed.price}')
            elif order.issell():
                self.log((f'SELL EXECUTED: {order.executed.price}'))

        self.bar_executed = len(self)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        print(' ')
        # print(f'### len self:\n {len(self)}')
        # print(f'### self.order: \n{self.order}')
        # print(f'### self.position: \n{self.position}')
        print(f'dataclose[0] = {self.dataclose[0]}')

        if self.order:
            return

        if not self.position:
            if self.dataclose[-1] < self.dataclose[-2] and \
               self.dataclose[0] < self.dataclose[-1]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log(f'SELL CREATED {self.dataclose[0]}')
                self.order = self.sell()


# if __name__ == '__main__':
#     # Create a cerebro entity
#     cerebro = bt.Cerebro()
#
#     # Add a strategy
#     cerebro.addstrategy(TestStrategy)
#
#     # Create a Data Feed
#     data = bt.feeds.YahooFinanceCSVData(
#         dataname='oracle.csv',
#         # Do not pass values before this date
#         fromdate=datetime.datetime(2000, 1, 1),
#         # Do not pass values before this date
#         todate=datetime.datetime(2000, 12, 31),
#         # Do not pass values after this date
#         reverse=False)
#
#     # Add the Data Feed to Cerebro
#     cerebro.adddata(data)
#
#     # Set our desired cash start
#     cerebro.broker.setcash(100000.0)
#
#     # Print out the starting conditions
#     print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
#
#     # Run over everything
#     cerebro.run()
#
#     # Print out the final result
#     print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
