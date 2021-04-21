from application.api.backtest.strategies.BaseStrategy import BaseStrategy
import backtrader as bt


class MaCrossoverStrategy(BaseStrategy):
    # Moving average parameters
    params = (('pfast', 34), ('pslow', 89),)

    def __init__(self):
        # Instantiate moving averages
        self.slow_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.pfast)
        ''' Using the built-in crossover indicator
        self.crossover = bt.indicators.CrossOver(self.slow_sma, self.fast_sma)'''
        super(MaCrossoverStrategy, self).__init__()

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         # An active Buy/Sell order has been submitted/accepted - Nothing to do
    #         return

    #     # Check if an order has been completed
    #     # Attention: broker could reject order if not enough cash
    #     if order.status in [order.Completed]:
    #         if order.isbuy():
    #             self.log('BUY EXECUTED, %.2f' % order.executed.price)
    #         elif order.issell():
    #             self.log('SELL EXECUTED, %.2f' % order.executed.price)
    #         self.bar_executed = len(self)

    #     elif order.status in [order.Canceled, order.Margin, order.Rejected]:
    #         self.log('Order Canceled/Margin/Rejected')

    #     # Reset orders
    #     self.order = None

    def next(self):
        ''' Logic for using the built-in crossover indicator

        if self.crossover > 0: # Fast ma crosses above slow ma
            pass # Signal for buy order
        elif self.crossover < 0: # Fast ma crosses below slow ma
            pass # Signal for sell order
        '''

        # Check for open orders
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # We are not in the market, look for a signal to OPEN trades

            # If the 20 SMA is above the 50 SMA
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                # self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                # self.order = self.buy()\
                self.buy()
            # Otherwise if the 20 SMA is below the 50 SMA
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                # self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                # self.order = self.sell()\
                self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log('CLOSE CREATE, %.2f' % self.dataclose[0])
                self.order = self.close()