import backtrader as bt

class ALMA(bt.Indicator):
    lines = ('alma',)

    params = dict(
                    period=40,
                    sigma=6,
                    offset=1,
                )
    def __init__(self):

        self.asize = self.p.period - 1
        self.m = self.p.offset * self.asize
        self.s = self.p.period  / self.p.sigma
        self.dss = 2 * self.s * self.s

    def next(self):
        try:
            wtd_sum = 0
            self.l.alma[0] = 0
            if len(self) >= self.asize:
                for i in range(self.p.period):
                    im = i - self.m
                    wtd = np.exp( -(im * im) / self.dss)
                    self.l.alma[0] += self.data[0 - self.p.period + i] * wtd
                    wtd_sum += wtd
                self.l.alma[0] = self.l.alma[0] / wtd_sum
                print(self.l.alma[0])

        except TypeError:
            self.l.alma[0] = 0
            return
