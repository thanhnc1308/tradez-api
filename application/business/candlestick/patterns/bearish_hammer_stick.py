from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class BearishHammerStick(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 1, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        is_bearish_hammer = open > close
        is_bearish_hammer = is_bearish_hammer and self.approximate_equal(open, high)
        is_bearish_hammer = is_bearish_hammer and (open - close) <= 2 * (close - low)

        return is_bearish_hammer
