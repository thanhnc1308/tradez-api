from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params
import backtrader as bt

class MaCrossoverStrategy(BaseStrategy):
    # Moving average parameters
    params = (('pfast', 30), ('pslow', 50),)

    def __init__(self):
        # Instantiate moving averages
        self.slow_ema = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.pslow)
        self.fast_ema = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.pfast)
        ''' Using the built-in crossover indicator
        self.crossover = bt.indicators.CrossOver(self.slow_ema, self.fast_ema)'''
        super(MaCrossoverStrategy, self).__init__()

    def should_buy(self):
        # If the fast EMA is above the slow EMA
        return self.fast_ema[0] > self.slow_ema[0] and self.fast_ema[-1] < self.slow_ema[-1]

    def should_sell(self):
        return self.fast_ema[0] < self.slow_ema[0] and self.fast_ema[-1] > self.slow_ema[-1]

def get_MaCrossoverStrategy_params(config):
    strategy_params = config.get('strategy_params')
    pfast = strategy_params.get('pfast') or 30
    pslow = strategy_params.get('pslow') or 50
    result = {
        'pfast': pfast,
        'pslow': pslow,
    }
    result = get_common_params(strategy_params, result)
    return result
