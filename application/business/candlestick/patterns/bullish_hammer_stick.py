from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class BullishHammerStick(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 1, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        is_bullish_hammer = close > open
        is_bullish_hammer = is_bullish_hammer and self.approximate_equal(close, high)
        is_bullish_hammer = is_bullish_hammer and (close - open) <= 2 * (open - low)

        return is_bullish_hammer
