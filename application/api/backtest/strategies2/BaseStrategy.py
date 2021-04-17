from datetime import datetime
import backtrader as bt

DEBUG = True
ENV = 'development'

class BaseStrategy(bt.Strategy):
    def __init__(self):
        self.order = None
        self.last_operation = "SELL"
        self.status = "DISCONNECTED"
        self.bar_executed = 0
        self.buy_price_close = None
        self.soft_sell = False
        self.hard_sell = False
        self.log("Base strategy initialized")

    def reset_sell_indicators(self):
        self.soft_sell = False
        self.hard_sell = False
        self.buy_price_close = None

    def notify_data(self, data, status, *args, **kwargs):
        self.status = data._getstatusname(status)
        print(self.status)
        if status == data.LIVE:
            self.log("LIVE DATA - Ready to trade")

    def short(self):
        if self.last_operation == "SELL":
            return

        if ENV == "development":
            self.log("Sell ordered: $%.2f" % self.data0.close[0])
            return self.sell()

        cash, value = self.broker.get_wallet_balance("BTC")
        amount = value*0.99
        self.log("Sell ordered: $%.2f. Amount %.6f %s - $%.2f USDT" % (self.data0.close[0],
                                                                       amount, "BTC", value), True)
        return self.sell(size=amount)

    def long(self):
        if self.last_operation == "BUY":
            return

        self.log("Buy ordered: $%.2f" % self.data0.close[0], True)
        self.buy_price_close = self.data0.close[0]
        price = self.data0.close[0]

        if ENV == "development":
            return self.buy()

        cash, value = self.broker.get_wallet_balance("USDT")
        amount = (value / price) * 0.99  # Workaround to avoid precision issues
        self.log("Buy ordered: $%.2f. Amount %.6f %s. Ballance $%.2f USDT" % (self.data0.close[0],
                                                                              amount, "BTC", value), True)
        return self.buy(size=amount)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED/SUBMITTED')
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED', True)

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.last_operation = "BUY"
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm), True)
                if ENV == "production":
                    print(order.__dict__)

            else:  # Sell
                self.last_operation = "SELL"
                self.reset_sell_indicators()
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm), True)

            # Sentinel to None: new orders allowed
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected: Status %s - %s' % (order.Status[order.status],
                                                                         self.last_operation), True)

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        color = 'green'
        if trade.pnl < 0:
            color = 'red'

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm), True)

    def log(self, txt, send_telegram=False, color=None):
        if not DEBUG:
            return

        value = datetime.now()
        if len(self) > 0:
            value = self.data0.datetime.datetime()

        if color:
            txt = f'txt {color}'

        print('[%s] %s' % (value.strftime("%d-%m-%y %H:%M"), txt))