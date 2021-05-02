import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class RSIDivergenceStrategy(BaseStrategy):
    params = (
        ('memory_size', 5),
    )

    def log(self, txt, dt=None, debug=False):
        if debug:
            dt = dt or self.datas[0].datetime.date(0)
            print("{}, {}".format(dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.wins = 0
        self.gross_profits = 0
        self.gross_losses = 0
        self.max_profit = 0
        self.max_drawdown = 0
        self.total_trades = 0
        self.percent_profitable = 0
        self.profit_factor = 0

        self.memory_size = self.params.memory_size
        self.data_memory = DataMemory(self.memory_size)
        self.rsi_memory = LineMemory(self.memory_size)

        self.rsi = rsi = bt.indicators.RSI(self.datas[0])
        #self.sma = bt.indicators.SmoothedMovingAverage(rsi, period=10)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: {}, Cost: {}, Comm: {}".format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                    )
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Price: {}, Cost: {}, Comm: {}".format(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                    )
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        if trade.pnl > 0:
            self.wins += 1
            self.gross_profits += trade.pnl
            if trade.pnl > self.max_profit:
                self.max_profit = trade.pnl
        else:
            self.gross_losses -= trade.pnl
            if trade.pnl < self.max_drawdown:
                self.max_drawdown = trade.pnl

        if self.total_trades:
            self.percent_profitable = self.wins / self.total_trades
        if self.gross_losses != 0:
            self.profit_factor = self.gross_profits / self.gross_losses
        else:
            self.profit_factor = self.gross_profits / 1

        self.log("ORDER PROFIT, GROSS: {}, NET: {}".format(
                trade.pnl, trade.pnlcomm
            )
        )

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Today's Open: {}, High: {}, Low: {}, Close: {}, RSI: {}".format(
            self.data_open[0],
            self.data_high[0],
            self.data_low[0],
            self.dataclose[0],
            self.rsi[0],
        ))

        self.data_memory.push(
            open=self.data_open[0],
            high=self.data_high[0],
            low=self.data_low[0],
            close=self.dataclose[0],
        )
        self.rsi_memory.push(self.rsi[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if (
            self.data_memory.current_size >= self.memory_size
            #and self.rsi_memory.memory[0] > 70
        ):
            #plt.figure()
            rsi_slope = self.get_line_slope(self.rsi_memory, 'RSI')
            price_slope = self.get_line_slope(self.data_memory.closes, 'Price')
            #plt.legend(loc='upper left')
            #plt.title("{} Day Price-RSI Function".format(self.memory_size))
            #plt.savefig(
            #    "{}/{}.png".format(
            #        self.images_dir, self.datas[0].datetime.date(0)
            #    )
            #)
            #plt.close('all')

            # Check if we are in the market
            if not self.position:
                if (
                    self.rsi_memory.memory[0] < 30
                    and rsi_slope > 0
                    and price_slope < 0
                ):
                #if self.rsi[0] < 30:
                    self.log("CREATE BUY ORDER, {}".format(self.dataclose[0]))
                    self.order = self.buy()
            else:
                if (
                    self.rsi_memory.memory[0] > 70
                    and rsi_slope < 0
                    and price_slope > 0
                ):
                #if self.rsi[0] > 70:
                    self.log("CREATE SELL ORDER, {}".format(self.dataclose[0]))
                    self.order = self.sell()
                    self.total_trades += 1

    def get_line_slope(self, memory, indicator=''):
        x, y, yspline, yderivative = memory.get_interpolation()
        slope, intercept = memory.get_linear_trend(yspline)
        ytrend = intercept + slope * x
        #plt.plot(x, yspline, label="{} Spline".format(indicator))
        #plt.plot(x, yderivative, label="{} Derivative".format(indicator))
        #plt.plot(x, ytrend, label="{} Tendency".format(indicator))
        return slope