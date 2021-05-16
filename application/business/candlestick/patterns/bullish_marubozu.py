from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class BullishMarubozu(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 1, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        return self.approximate_equal(close, high) and self.approximate_equal(low, open) and open < close and open < high
