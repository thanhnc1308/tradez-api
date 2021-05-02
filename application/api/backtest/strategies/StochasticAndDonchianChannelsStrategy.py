import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class StochasticAndDonchianChannelsStrategy(BaseStrategy):
    '''Trading strategy that utilizes the Stochastic Oscillator indicator for oversold/overbought entry points, 
    and previous support/resistance via Donchian Channels as well as a max loss in pips for risk levels.'''
    # parameters for Stochastic Oscillator and max loss in pips
    # Donchian Channels to determine previous support/resistance levels will use the given period as well
    # http://www.ta-guru.com/Book/TechnicalAnalysis/TechnicalIndicators/Stochastic.php5 for Stochastic Oscillator formula and description
    params = (
        ('period', 14),
        ('pfast', 3),
        ('pslow', 3),
        ('upper_limit', 80),
        ('lower_limit', 20),
        ('stop_pips', .002)
    )

    def __init__(self):
        '''Initializes logger and variables required for the strategy implementation.'''

        self.donchian_stop_price = None
        self.price = None
        self.stop_price = None
        self.stop_donchian = None

        self.stochastic = bt.indicators.Stochastic(self.data, period=self.params.period, period_dfast=self.params.pfast, period_dslow=self.params.pslow,
        upperband=self.params.upper_limit, lowerband=self.params.lower_limit)
        super(StochasticAndDonchianChannelsStrategy, self).__init__()

    def next(self):
        '''Checks to see if Stochastic Oscillator, position, and order conditions meet the entry or exit conditions for the execution of buy and sell orders.'''
        if self.order:
            # if there is a pending order, don't do anything
            return
        if self.position.size == 0:
            # When stochastic crosses back below 80, enter short position.
            if self.stochastic.lines.percD[-1] >= 80 and self.stochastic.lines.percD[0] <= 80:
                # stop price at last support level in self.params.period periods
                self.donchian_stop_price = max(self.data.high.get(size=self.params.period))
                self.order = self.sell()
                # stop loss order for max loss of self.params.stop_pips pips
                self.stop_price = self.buy(exectype=bt.Order.Stop, price=self.data.close[0]+self.params.stop_pips, oco=self.stop_donchian)
                # stop loss order for donchian SR price level
                self.stop_donchian = self.buy(exectype=bt.Order.Stop, price=self.donchian_stop_price, oco=self.stop_price)
            # when stochastic crosses back above 20, enter long position.
            elif self.stochastic.lines.percD[-1] <= 20 and self.stochastic.lines.percD[0] >= 20:
                # stop price at last resistance level in self.params.period periods
                self.donchian_stop_price = min(self.data.low.get(size=self.params.period))
                self.order = self.buy()
                # stop loss order for max loss of self.params.stop_pips pips
                self.stop_price = self.sell(exectype=bt.Order.Stop, price=self.data.close[0]-self.params.stop_pips, oco=self.stop_donchian)
                # stop loss order for donchian SR price level
                self.stop_donchian = self.sell(exectype=bt.Order.Stop, price=self.donchian_stop_price, oco=self.stop_price)

        if self.position.size > 0:
            # When stochastic is above 70, close out of long position
            if (self.stochastic.lines.percD[0] >= 70):
                self.close(oco=self.stop_price)
        if self.position.size < 0:
            # When stochastic is below 30, close out of short position
            if (self.stochastic.lines.percD[0] <= 30):
                self.close(oco=self.stop_price)

def get_StochasticAndDonchianChannelsStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    pfast = strategy_params.get('pfast') or 3
    pslow = strategy_params.get('pslow') or 3
    upper_limit = strategy_params.get('upper_limit') or 80
    lower_limit = strategy_params.get('lower_limit') or 20
    stop_pips = strategy_params.get('stop_pips') or .002
    result = {
        'period': period,
        'pfast': pfast,
        'pslow': pslow,
        'upper_limit': upper_limit,
        'lower_limit': lower_limit,
        'stop_pips': stop_pips
    }
    return result
