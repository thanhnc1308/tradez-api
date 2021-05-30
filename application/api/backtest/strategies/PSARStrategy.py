from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params
import backtrader as bt

class PSARStrategy(BaseStrategy):
    params = (
        ('period', 2),
        ('af', 0.02),
        ('afmax', 0.2),
    )

    def __init__(self):
        self.psar = bt.indicators.PSAR(self.datas[0])
        self.is_previous_psar_below_price = False
        super(PSARStrategy, self).__init__()

    def next(self):
        if self.psar[-1] < self.dataclose:
            self.is_previous_psar_below_price = True
        elif self.psar[-1] > self.dataclose:
            self.is_previous_psar_below_price = False
        super(PSARStrategy, self).next()

    def should_buy(self):
        # print(self.psar[0])
        return not self.is_previous_psar_below_price and self.psar[0] < self.dataclose

    def should_sell(self):
        return self.is_previous_psar_below_price and self.psar[0] > self.dataclose

def get_PSARStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 2
    af = strategy_params.get('af') or 0.02
    afmax = strategy_params.get('afmax') or 0.2
    result = {
        'period': period,
        'af': af,
        'afmax': afmax,
    }
    result = get_common_params(strategy_params, result)
    return result
