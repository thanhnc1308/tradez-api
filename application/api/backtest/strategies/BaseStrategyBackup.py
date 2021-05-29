import datetime
import backtrader as bt


class BaseStrategy(bt.Strategy):

    params = (
        ('atr_stop_loss', 1.5),
        ('atr_scale_out', 1 )
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # print(self.datas[0].volume)
        # self.atr14 = self.datas[0].atr14

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.atr14 = bt.indicators.ATR(self.data, period=14)
        self.stop_loss_level = None
        self.scale_out_level = None

        self.orefs = None

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

    def next(self):
        '''Runs for every candlestick. Checks conditions to enter and exit trades.'''
        # from settings import CONFIG
        from application.api.backtest.settings import CONFIG

        # Simply log the closing price of the series from the reference
        if CONFIG['log']:
            self.log('Close, %.2f' % self.dataclose[0])

    def buy(self):
        # from settings import CONFIG
        from application.api.backtest.settings import CONFIG
        close = self.dataclose[0]

        if CONFIG['take_profit']['enabled'] or CONFIG['stop_loss']['enabled']:

            aux_orefs = []
            limit = 0.005 # TODO: settings
            p1 = close * (1.0 - limit)
            p2 = p1 - CONFIG['stop_loss']['value'] * close
            p3 = p1 + CONFIG['take_profit']['value'] * close

            limdays = 3 # TODO: settings
            limdays2 = 1000 # TODO: settings
            valid1 = datetime.timedelta(limdays)
            valid2 = valid3 = datetime.timedelta(limdays2)

            o1 = super(BaseStrategy, self).buy(exectype=bt.Order.Limit,
                                           price=p1,
                                           valid=valid1,
                                           transmit=False,
                                           size=CONFIG['size'])
            # self.log('BUY CREATE, %.2f' % p1)
            self.trade_result.append({
                'transaction_type': 'BUY CREATE',
                'transaction_date': self.get_date_format(),
                'price': p1
            })
            aux_orefs.append(o1.ref)

            if CONFIG['stop_loss']['enabled']:
                o2 = super(BaseStrategy, self).sell(exectype=bt.Order.Stop,
                                                price=p2,
                                                valid=valid2,
                                                parent=o1,
                                                transmit=False,
                                                size=CONFIG['size'])
                # self.log('STOP LOSS CREATED, %.2f' % p2)
                self.trade_result.append({
                    'transaction_type': 'STOP LOSS CREATED',
                    'transaction_date': self.get_date_format(),
                    'price': p2
                })
                aux_orefs.append(o2.ref)

            if CONFIG['take_profit']['enabled']:
                o3 = super(BaseStrategy, self).sell(exectype=bt.Order.Limit,
                                                price=p3,
                                                valid=valid3,
                                                parent=o1,
                                                transmit=True,
                                                size=CONFIG['size'])
                # self.log('TAKE PROFIT CREATED, %.2f' % p3)
                self.trade_result.append({
                    'transaction_type': 'TAKE PROFIT CREATED',
                    'transaction_date': self.get_date_format(),
                    'price': p3
                })
                aux_orefs.append(o3.ref)

            self.orefs = aux_orefs

        else:
            # self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.trade_result.append({
                'transaction_type': 'BUY CREATE',
                'transaction_date': self.get_date_format(),
                'price': self.dataclose[0]
            })
            self.stop_loss_level = self.dataclose - self.atr14 * self.params.atr_stop_loss
            self.scale_out_level = self.dataclose + self.atr14 * self.params.atr_scale_out
            self.order = super(BaseStrategy, self).buy(size=CONFIG['size'])

    def sell(self, sell_type='scale_out'):
        # from settings import CONFIG
        from application.api.backtest.settings import CONFIG

        if not CONFIG['take_profit']['enabled'] and not CONFIG['stop_loss']['enabled']:
            # self.log('SELL CREATE, %.2f' % self.dataclose[0])
            self.trade_result.append({
                'transaction_type': 'SELL CREATE',
                'transaction_date': self.get_date_format(),
                'sell_type': sell_type,
                'price': self.dataclose[0]
            })
            self.order = super(BaseStrategy, self).sell(size=CONFIG['size'])
            self.stop_loss_level = None
            self.scale_out_level = None

    def next(self):
        if not self.position:
            if self.should_buy():
                # print(self.atr14)
                # print(self.dataclose - self.atr14)
                # print(self.dataclose - self.datas[0].atr14)
                # print(self.params.atr_scale_out)
                self.buy()
        else:
            self.position
            self.in_position()
            # if self.rsi > self.params.lower:
            #     self.sell()

    def should_buy(self):
        return False

    def should_sell(self):
        return False

    def in_position(self):
        if self.dataclose <= self.stop_loss_level:
                self.stop_loss()
        elif self.dataclose >= self.scale_out_level:
            self.scale_out()

    def stop_loss(self):
        self.trade_result.append({
            'transaction_type': 'STOP LOSS CREATE',
            'transaction_date': self.get_date_format(),
            'price': self.dataclose[0]
        })
        self.order = super(BaseStrategy, self).sell()

    def scale_out(self):
        self.trade_result.append({
            'transaction_type': 'SCALE OUT CREATE',
            'transaction_date': self.get_date_format(),
            'price': self.dataclose[0]
        })
        self.order = super(BaseStrategy, self).sell()

    def notify_order(self, order):
        '''Run on every next iteration, logs the order execution status whenever an order is filled or rejected, 
        setting the order parameter back to None if the order is filled or cancelled to denote that there are no more pending orders.'''
        # from settings import CONFIG
        from application.api.backtest.settings import CONFIG

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        # if order.status in [order.Completed, order.Canceled, order.Margin]:
        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log(
                #     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #     (order.executed.price,
                #      order.executed.value,
                #      order.executed.comm))
                self.trade_result.append({
                    'transaction_type': 'BUY EXECUTED',
                    'transaction_date': self.get_date_format(),
                    'price': order.executed.price,
                    'cost': order.executed.value,
                    'size': order.executed.size,
                    'buytime': bt.num2date(order.executed.dt),
                    'commission': order.executed.comm,
                })
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                # self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #          (order.executed.price,
                #           order.executed.value,
                #           order.executed.comm))
                self.trade_result.append({
                    'transaction_type': 'SELL EXECUTED',
                    'transaction_date': self.get_date_format(),
                    'price': order.executed.price,
                    'cost': order.executed.value,
                    'size': order.executed.size,
                    'buytime': bt.num2date(order.executed.dt),
                    'commission': order.executed.comm,
                })
            self.bar_executed = len(self)
        elif order.status in [order.Rejected, order.Canceled, order.Margin]:
            # print('%s ,' % order.Status[order.status])
            pass

        if CONFIG['stop_loss']['enabled'] or CONFIG['take_profit']['enabled']:
            if not order.alive() and order.ref in self.orefs:
                self.orefs = []
        else:
            # Write down: no pending order
            self.order = None

    def notify_trade(self, trade):
        '''Run on every next iteration. Logs data on every trade when closed.'''
        if not trade.isclosed:
            return

        # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
        #          (trade.pnl, trade.pnlcomm))
        self.trade_result.append({
            'transaction_type': 'OPERATION PROFIT',
            'transaction_date': self.get_date_format(),
            'gross': trade.pnl,
            'net': trade.pnlcomm
        })
        if trade.pnlcomm >= 0:
            self.win_quantity += 1
        else:
            self.loss_quantity += 1

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