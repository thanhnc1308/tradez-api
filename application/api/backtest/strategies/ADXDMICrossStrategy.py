from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params
import backtrader as bt


class ADXDMICrossStrategy(BaseStrategy):

    params = (
        ('period', 14),
        ('adx_strong_trend_level', 25),
    )

    def __init__(self):
        self.adx = bt.ind.ADX(self.data, period=self.params.period)
        self.dmiplus, self.dmimin = bt.ind.PlusDI(), bt.ind.MinusDI()
        # self.crossoverdmi = bt.ind.CrossOver(self.dmimin, self.dmiplus)
        super(ADXDMICrossStrategy, self).__init__()

    def should_buy(self):
        return self.dmiplus > self.dmimin and self.adx[0] > self.params.adx_strong_trend_level

    def should_sell(self):
        return self.dmiplus < self.dmimin and self.adx[0] > self.params.adx_strong_trend_level

    # def next(self):
    #     #     if self.crossoverdmi[0] == -1.0 and self.adx[0] > ADX:
    #     if self.dmiplus > self.dmimin and self.adx[0] > ADX:
    #         self.buy()
    #     #     if self.datas[0].datetime.date(0) == datetime(2020, 1, 23).date():
    #     if self.dmiplus < self.dmimin and self.adx[0] > ADX:
    #         self.close()


def get_ADXDMICrossStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period = strategy_params.get('period') or 14
    adx_strong_trend_level = strategy_params.get('adx_strong_trend_level') or 25
    result = {
        'period': period,
        'adx_strong_trend_level': adx_strong_trend_level,
    }
    result = get_common_params(strategy_params, result)
    return result
