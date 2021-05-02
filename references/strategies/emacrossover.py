import backtrader as bt
import backtrader.indicators as btind

class EMACrossOver(bt.Strategy):
    params = dict(
        fast=50,
        slow=100,
        long=200,
        printout=False,
        longonly=False,
        BuyLast=False
    )

    def log(self, txt, dt=None):
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            dt = bt.num2date(dt)
            print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.orderid = None  # to control operation entries

        fast_ema = btind.EMA(period=self.p.fast)
        slow_ema = btind.EMA(period=self.p.slow)
        long_ema = btind.EMA(period=self.p.long)
        self.signal = btind.CrossOver(fast_ema, slow_ema)
        self.log(f'Initial portfolio value of {self.broker.get_value():.2f}\n')

    def start(self):
        pass

    def next(self):
        if self.orderid:
            return  # if an order is active, no new orders are allowed

        # Buy when price above long EMA and fast EMA crosses above slow EMA
        if self.data.close[0] > self.long_ema[0] and self.signal > 0.0:
            self.log(f'BUY {self.getsizing()} shares of {self.data._name} at {self.data.close[0]}')
            self.buy()
            self.p.BuyLast = True
            self.orderid = 1
            self.sell_price = (self.data.close[0]-self.long_ema[0]) * 1.5 + self.data.close[0]

        # Sell when price below long EMA and fast EMA crosses below slow EMA
        elif self.data.close[0] < self.long_ema[0] and self.signal < 0.0:
            if not self.p.longonly:
                self.log(f'SELL {abs(self.getsizing())} shares '
                         f'of {self.data._name} at {self.data.close[0]}')
                self.sell()
                self.p.BuyLast = False
                self.orderid = 2
                self.buy_price = self.data.close[0] - (self.long_ema[0]-self.data.close[0]) * 1.5
                if self.buy_price < 0:
                    raise Exception("ERROR")

        # Close long position
        elif self.orderid == 1 and self.data.close[0] >= self.sell_price:
            if self.position:
                self.log(f'CLOSE LONG position of {self.position.size} shares '
                         f'of {self.data._name} at {self.data.close[0]:.2f}')
                self.close()
                self.orderid = None

        # Close short position
        elif self.orderid == 2 and self.data.close[0] >= self.sell_price:
            if self.position:
                self.log(f'CLOSE SHORT position of {abs(self.position.size)} shares '
                         f'of {self.data._name} at {self.data.close[0]:.2f}')
                self.close()
                self.orderid = None


    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = f'BUY COMPLETED. ' \
                         f'Size: {order.executed.size}, ' \
                         f'Price: {order.executed.price:.2f}, ' \
                         f'Commission: {order.executed.comm:.2f}'
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETED. ' \
                         f'Size: {abs(order.executed.size)}, ' \
                         f'Price: {order.executed.price:.2f}, ' \
                         f'Commission: {order.executed.comm:.2f}'
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log(f'{order.Status[order.status]}')
            pass  # Simply log

        # Allow new orders
        self.orderid = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(f'TRADE COMPLETED, '
                     f'Portfolio: {self.broker.get_value():.2f}, '
                     f'Gross: {trade.pnl:.2f}, '
                     f'Net: {trade.pnlcomm:.2f}')

        elif trade.justopened:
            #self.log('TRADE OPENED, SIZE %2d' % trade.size)
            pass
