import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy, get_common_params


class MACDStrategy(BaseStrategy):

    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),
    )

    def __init__(self):
        # Keep a reference to the "close" and "volume" line in the data[0] dataseries
        # self.dataclose = self.datas[0].close
        # self.datavolume = self.datas[0].volume

        # self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.period)

        # Indicators
        # self.macd = MACD2()
        self.macd = bt.indicators.MACDHistogram(self.data,
                                       period_me1=self.p.period_me1,
                                       period_me2=self.p.period_me2,
                                       period_signal=self.p.period_signal)
        self.last_macd_histo = None
        self.macd_going_up = False
        self.macd_going_down = False

        super(MACDStrategy, self).__init__()

    def next(self):
        # macd_macd = self.macd.lines.macd[0]
        # macd_signal = self.macd.lines.signal[0]
        # self.log('MACD       , %.2f' % macd_macd)
        # self.log('MACD-SIGNAL, %.2f' % macd_signal)

        self.macd_going_up = False
        self.macd_going_down = False

        print(self.macd.lines.__dict__.keys())
        print(self.macd.lines.__str__())
        print(self.macd.lines.__dict__.items())
        print(self.macd.lines)

        # grow_rate = 0
        if self.last_macd_histo is not None:
            histo = self.macd.lines.histo[0]
            grow_rate = histo - self.last_macd_histo

            # self.log('Grow Rate,  %s' % grow_rate)
            if histo > 0 and self.last_macd_histo < 0:
                self.macd_going_up = True
                self.macd_going_down = False
            elif histo < 0 and self.last_macd_histo > 0:
                self.macd_going_up = False
                self.macd_going_down = True

            # if (histo > 0) and (grow_rate > 20):
            #     self.macd_going_up = True
            #     self.macd_going_down = False
            # elif histo < 1:
            #     self.macd_going_up = False
            #     self.macd_going_down = True

        self.last_macd_histo = self.macd.lines.histo[0]

        super(MACDStrategy, self).next()

        # if self.macd_going_up:
        #     self.log('GOING UP, histogram: %s, grow rate: %s' % (histo, grow_rate))
        # if self.macd_going_down:
        #     self.log('GOING DOWN, histogram: %s, grow rate: %s' % (histo, grow_rate))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        # if self.order:
        #     return

        # Check if we are in the market
        # if not self.position:
        #     # Not yet ... we MIGHT BUY if ...
        #     if self.macd_going_up:
        #         # BUY, BUY, BUY!!! (with all possible default parameters)
        #         self.log('BUY CREATE, %.2f' % (self.dataclose[0]))

        #         # Keep track of the created order to avoid a 2nd order
        #         self.order = self.buy()

        # else:
        #     if self.macd_going_down:
        #         # SELL, SELL, SELL!!! (with all possible default parameters)
        #         self.log('SELL CREATE, %.2f' % self.dataclose[0])

        #         # Keep track of the created order to avoid a 2nd order
        #         self.order = self.sell()

    def should_buy(self):
        return self.macd_going_up

    def should_sell(self):
        return self.macd_going_down


# class MACD2(bt.indicators.MACDHisto):
#     ''' MACD2 uses Simple moving average instead of Exponential one '''
#     params = (('period_me1', 12), ('period_me2', 26), ('period_signal', 9),
#               ('movav', MovAv.Simple),)


def get_MACDStrategy_params(config):
    strategy_params = config.get('strategy_params')
    period_me1 = strategy_params.get('period_me1') or 12
    period_me2 = strategy_params.get('period_me2') or 26
    period_signal = strategy_params.get('period_signal') or 9
    result = {
        'period_me1': period_me1,
        'period_me2': period_me2,
        'period_signal': period_signal
    }
    result = get_common_params(strategy_params, result)
    return result
