import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class BollingerBandsAndRSIStrategy(BaseStrategy):
    """Bollinger Bands Strategy
    """

    params = (
        ('bbband_period', 20),
        ('devfactor', 2),
        ('rsi_period', 14),
        ('upper', 70),
        ('lower', 30),
    )

    def __init__(self):
        # Add a BBand indicator
        self.bband = bt.indicators.BBands(self.datas[0],
                                          period=self.params.bbband_period,
                                          devfactor=self.params.devfactor)
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.rsi_period)
        super(BollingerBandsAndRSIStrategy, self).__init__()

    def next(self):
        super(BollingerBandsAndRSIStrategy, self).next()

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if self.orefs:
            return

        if self.dataclose < self.bband.lines.bot and not self.position and self.rsi < self.params.lower:
            self.buy()

        if self.dataclose > self.bband.lines.top and self.position and self.rsi > self.params.upper:
            self.sell()

    # def stop(self):
        # from settings import CONFIG
        # from application.api.backtest.settings import CONFIG
        # pnl = round(self.broker.getvalue() - CONFIG['capital_base'], 2)
        # print('Aberration Period: {} Final PnL: {}'.format(
        #     self.params.period, pnl))

def get_BollingerBandsAndRSIStrategy_params(config):
    strategy_params = config.get('strategy_params')
    bbband_period = strategy_params.get('bbband_period') or 20
    devfactor = strategy_params.get('devfactor') or 2
    rsi_period = strategy_params.get('rsi_period') or 14
    upper = strategy_params.get('upper') or 70
    lower = strategy_params.get('lower') or 30
    result = {
        'bbband_period': bbband_period,
        'devfactor': devfactor,
        'rsi_period': rsi_period,
        'upper': upper,
        'lower': lower
    }
    return result
