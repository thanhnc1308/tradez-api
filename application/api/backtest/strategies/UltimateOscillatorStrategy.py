import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class UltimateOscillatorStrategy(BaseStrategy):

    params = (
        ('p1', 7),
        ('p2', 14),
        ('p3', 28),
        ('upper', 70),
        ('lower', 30),
    )

    def __init__(self):
        self.ultimate_oscillator = bt.indicators.UltimateOscillator(
            self.data,
            p1=self.params.p1,
            p2=self.params.p2,
            p3=self.params.p3
        )
        super(UltimateOscillatorStrategy, self).__init__()

    def next(self):
        self.log(f'self.ultimate_oscillator: {self.ultimate_oscillator[0]}')
        super(UltimateOscillatorStrategy, self).next()

    def should_buy(self):
        return self.ultimate_oscillator > self.params.upper

    def should_sell(self):
        return self.ultimate_oscillator < self.params.lower


def get_UltimateOscillatorStrategy_params(config):
    strategy_params = config.get('strategy_params')
    p1 = strategy_params.get('p1') or 14
    p2 = strategy_params.get('p2') or 14
    p3 = strategy_params.get('p3') or 14
    upper = strategy_params.get('upper') or 70
    lower = strategy_params.get('lower') or 30
    result = {
        'p1': p1,
        'p2': p2,
        'p3': p3,
        'upper': upper,
        'lower': lower
    }
    result = get_common_params(strategy_params, result)
    return result
