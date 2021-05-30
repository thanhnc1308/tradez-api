import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class BollingerBandsStrategy(BaseStrategy):
    """Bollinger Bands Strategy
    """

    params = (
        ('period', 20),
        ('devfactor', 2),
    )

    def __init__(self):
        # Add a BBand indicator
        self.bband = bt.indicators.BBands(self.datas[0],
                                          period=self.params.period,
                                          devfactor=self.params.devfactor)
        super(BollingerBandsStrategy, self).__init__()

    # def next(self):
    #     super(BollingerBandsStrategy, self).next()

    #     # Check if an order is pending ... if yes, we cannot send a 2nd one
    #     if self.order:
    #         return

    #     if self.orefs:
    #         return

    #     if self.dataclose < self.bband.lines.bot and not self.position:
    #         self.buy()

    #     if self.dataclose > self.bband.lines.top and self.position:
    #         self.sell()

    # def next(self):
    #     super(BollingerBandsStrategy, self).next()
    #     if not self.is_in_position:
    #         if self.should_buy():
    #             self.buy()
    #         elif self.should_sell():
    #             self.sell()
    #     else:
    #         self.manage_exist_trade()

    def should_buy(self):
        return self.dataclose < self.bband.lines.bot

    def should_sell(self):
        return self.dataclose > self.bband.lines.top

    # def stop(self):
    #     # from settings import CONFIG
    #     from application.api.backtest.settings import CONFIG
    #     pnl = round(self.broker.getvalue() - CONFIG['capital_base'], 2)
    #     print('BollingerBandsStrategy Period: {} Final PnL: {}'.format(
    #         self.params.period, pnl))

def get_BollingerBandsStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 20
    devfactor = strategy_params.get('devfactor') or 2
    result = {
        'period': period,
        'devfactor': devfactor
    }
    result = get_common_params(strategy_params, result)
    return result
