import datetime
import backtrader as bt
from application.business.indicators.volatility import average_true_range, bollinger_hband_indicator, bollinger_lband_indicator, keltner_channel_hband_indicator, keltner_channel_lband_indicator

# class ATR(bt.Indicator):
#     lines = ('atr',)

#     params = (('period', 14),)

#     def __init__(self):
#         self.lines.atr = average_true_range(high=self.datas[0].high, low=self.datas[0].low, close=self.datas[0].close, window=14)

    # def next(self):
    #     self.lines.atr[0] = average_true_range(high=self.data.high, low=self.data.low, close=self.data.close, window=14)

class BaseStrategy(bt.Strategy):

    params = (
        ('atr_stop_loss', 1.5),
        ('atr_scale_out', 1 )
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        # buy/sell
        self.order_type = None
        self.is_in_position = False

        self.atr14 = bt.indicators.ATR(self.data, period=14)
        self.stop_loss_level = None
        self.scale_out_level = None

        self.trade_result = []
        self.win_quantity = 0
        self.loss_quantity = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def get_date_format(self):
        return self.datas[0].datetime.date(0).isoformat()

    def get_trade_result(self):
        return self.trade_result

    def get_win_rate(self):
        total_trades = self.win_quantity + self.loss_quantity or 1
        return round(self.win_quantity / (total_trades) * 100, 2)

    def get_total_trades(self):
        return self.win_quantity + self.loss_quantity

    def buy(self):
        self.stop_loss_level = self.dataclose - self.atr14 * self.params.atr_stop_loss
        self.scale_out_level = self.dataclose + self.atr14 * self.params.atr_scale_out
        self.trade_result.append({
            'transaction_type': 'BUY CREATE',
            'transaction_date': self.get_date_format(),
            'price': self.dataclose[0],
            'stop_loss_level': self.stop_loss_level,
            'scale_out_level': self.scale_out_level,
        })
        self.is_in_position = True
        self.order_type = 'buy'
        # self.order = super(BaseStrategy, self).buy()

    def sell(self):
        self.stop_loss_level = self.dataclose + self.atr14 * self.params.atr_stop_loss
        self.scale_out_level = self.dataclose - self.atr14 * self.params.atr_scale_out
        self.trade_result.append({
            'transaction_type': 'SELL CREATE',
            'transaction_date': self.get_date_format(),
            'price': self.dataclose[0],
            'stop_loss_level': self.stop_loss_level,
            'scale_out_level': self.scale_out_level,
        })
        self.is_in_position = True
        self.order_type = 'sell'
        # self.order = super(BaseStrategy, self).sell()

    def next(self):
        if not self.is_in_position:
            if self.should_buy():
                self.buy()
            elif self.should_sell():
                self.sell()
        else:
            self.manage_exist_trade()

    def should_buy(self):
        return False

    def should_sell(self):
        return False

    def manage_exist_trade(self):
        if self.order_type == 'buy':
            if self.dataclose <= self.stop_loss_level:
                self.stop_loss()
            elif self.dataclose >= self.scale_out_level:
                self.scale_out()
        elif self.order_type == 'sell':
            if self.dataclose >= self.stop_loss_level:
                self.stop_loss()
            elif self.dataclose <= self.scale_out_level:
                self.scale_out()

    def stop_loss(self):
        self.trade_result.append({
            'transaction_type': 'STOP LOSS CREATE',
            'transaction_date': self.get_date_format(),
            'price': self.dataclose[0]
        })
        self.is_in_position = False
        self.loss_quantity += 1

    def scale_out(self):
        self.trade_result.append({
            'transaction_type': 'SCALE OUT CREATE',
            'transaction_date': self.get_date_format(),
            'price': self.dataclose[0]
        })
        self.is_in_position = False
        self.win_quantity += 1

    def notify_order(self, order):
        '''Run on every next iteration, logs the order execution status whenever an order is filled or rejected, 
        setting the order parameter back to None if the order is filled or cancelled to denote that there are no more pending orders.'''

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        # if order.status in [order.Completed, order.Canceled, order.Margin]:
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
            else:
                pass
        elif order.status in [order.Rejected, order.Canceled, order.Margin]:
            # print('%s ,' % order.Status[order.status])
            pass
        else:
            # Write down: no pending order
            self.order = None

    def notify_trade(self, trade):
        '''Run on every next iteration. Logs data on every trade when closed.'''
        if not trade.isclosed:
            return

    def stop(self):
        '''At the end of the strategy backtest, logs the ending value of the portfolio as well as one or multiple parameter values for strategy optimization purposes.'''
        self.log('End of the strategy')
        # self.log('(bbma: {}, bbsd: {}, adxper: {}) Ending Value: {}'.format(self.params.BB_MA, self.params.BB_SD, self.params.ADX_Period, self.broker.getvalue()), doprint=True)
        # fields = [[self.params.BB_MA, self.params.BB_SD, self.params.ADX_Period, self.broker.getvalue()]]
        # df = pd.DataFrame(data=fields)
        # df.to_csv('optimization.csv', mode='a', index=False, header=False)


def get_common_params(strategy_params, result):
    atr_stop_loss = strategy_params.get('atr_stop_loss') or 1.5
    atr_scale_out = strategy_params.get('atr_scale_out') or 1
    result['atr_stop_loss'] = atr_stop_loss
    result['atr_scale_out'] = atr_scale_out
    return result