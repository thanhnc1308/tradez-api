import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class BollingerBandsAndADXStrategy(BaseStrategy):
    '''Mean Reversion trading strategy that utilizes Bollinger Bands for signals and ADX for locating and avoiding trends'''

    # Parameters that can be optimized for best performance for different markets or candlestick timeframes
    params = (
        ('bbband_period', 20),
        ('bbband_devfactor', 2),
        ('adx_period', 14),
        ('adx_max', 40)
    )

    def __init__(self):
        '''Initializes all variables to be used in this strategy'''
        self.stop_price = None
        self.close_position = None
        self.adx = bt.indicators.AverageDirectionalMovementIndex(self.data, period=self.params.adx_period)
        self.bb = bt.indicators.BollingerBands(self.data, period=self.params.bbband_period, bbband_devfactor=self.params.bbband_devfactor)
        super(BollingerBandsAndADXStrategy, self).__init__()

    def next(self):
        '''Runs for every candlestick. Checks conditions to enter and exit trades.'''
        if self.order:
            return
        if self.position.size == 0:
            if self.adx[0] < self.params.adx_max:
                if (self.data.close[-1] > self.bb.lines.top[-1]) and (self.data.close[0] <= self.bb.lines.top[0]):
                    self.sell()
                    # self.order = self.sell()
                    # self.stop_price = self.bb.lines.top[0]
                    # self.close_position = self.buy(exectype=bt.Order.Stop, price=self.stop_price)

                elif (self.data.close[-1] < self.bb.lines.bot[-1]) and (self.data.close[0] >= self.bb.lines.bot[0]):
                    self.buy()
                    # self.order = self.buy()
                    # self.stop_price = self.bb.lines.bot[0]
                    # self.close_position = self.sell(exectype=bt.Order.Stop, price=self.stop_price)

        elif self.position.size > 0:
            if (self.data.close[-1] < self.bb.lines.mid[-1]) and (self.data.close[0] >= self.bb.lines.mid[0]):
                self.close_position = self.close()
        elif self.position.size < 0:
            if (self.data.close[-1] > self.bb.lines.mid[-1]) and (self.data.close[0] <= self.bb.lines.mid[0]):
                self.close_position = self.close()

def get_BollingerBandsAndADXStrategy_params(config):
    strategy_params = config.get('strategy_params')
    bbband_period = strategy_params.get('bbband_period') or 20
    bbband_devfactor = strategy_params.get('bbband_devfactor') or 2
    adx_period = strategy_params.get('adx_period') or 30
    adx_max = strategy_params.get('adx_max') or 40
    result = {
        'bbband_period': bbband_period,
        'bbband_devfactor': bbband_devfactor,
        'adx_period': adx_period,
        'adx_max': adx_max
    }
    return result
