import backtrader as bt
from application.api.backtest.strategies.BaseStrategy import BaseStrategy


class MACDStrategy(BaseStrategy):

    def __init__(self):
        # Keep a reference to the "close" and "volume" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume

        # Indicators
        self.macd = MACD2()

        # To keep track of pending orders and buy price/commission
        self.order = None

        self.last_macd_histo = None

    def next(self):
        macd_macd = self.macd.lines.macd[0]
        macd_signal = self.macd.lines.signal[0]
        self.log('MACD       , %.2f' % macd_macd)
        self.log('MACD-SIGNAL, %.2f' % macd_signal)

        macd_going_up = False
        macd_going_down = False

        grow_rate = 0
        if self.last_macd_histo is not None:
            histo = self.macd.lines.histo[0]
            grow_rate = histo - self.last_macd_histo

            self.log('Grow Rate,  %s' % grow_rate)

            if (histo > 0) and (grow_rate > 20):
                macd_going_up = True
                macd_going_down = False
            elif histo < 1:
                macd_going_up = False
                macd_going_down = True

        self.last_macd_histo = self.macd.lines.histo[0]

        if macd_going_up:
            self.log('GOING UP, histogram: %s, grow rate: %s' % (histo, grow_rate))
        if macd_going_down:
            self.log('GOING DOWN, histogram: %s, grow rate: %s' % (histo, grow_rate))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if macd_going_up:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % (self.dataclose[0]))

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:
            if macd_going_down:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class MACD2(bt.indicators.MACDHisto):
    ''' MACD2 uses Simple moving average instead of Exponential one '''
    params = (('period_me1', 12), ('period_me2', 26), ('period_signal', 9),
              ('movav', MovAv.Simple),)
