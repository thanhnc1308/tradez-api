from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params
import backtrader as bt

class JapaneseCandlestickStrategy(BaseStrategy):
    params = (
        ('pattern', 'pinbar'),
    )

    def __init__(self):
        if self.params.pattern == 'pinbar':
            self.pinbar = bt.talib.CDLDOJI(self.data.open, self.data.high, self.data.low, self.data.close)
        elif self.params.pattern == 'engufling':
            pass
        elif self.params.pattern == 'marubozu':
            pass
        super(JapaneseCandlestickStrategy, self).__init__()

    # def next(self):
    #     if self.psar[-1] < self.dataclose:
    #         self.is_previous_psar_below_price = True
    #     elif self.psar[-1] > self.dataclose:
    #         self.is_previous_psar_below_price = False
    #     super(JapaneseCandlestickStrategy, self).next()

    def should_buy(self):
        return not self.is_previous_psar_below_price and self.psar[0] < self.dataclose

    def should_sell(self):
        return self.is_previous_psar_below_price and self.psar[0] > self.dataclose

def get_JapaneseCandlestickStrategy_params(config):
    strategy_params = config.get('strategy_params')
    pattern = strategy_params.get('af') or 'pinbar'
    result = {
        'pattern': pattern,
    }
    result = get_common_params(strategy_params, result)
    return result
