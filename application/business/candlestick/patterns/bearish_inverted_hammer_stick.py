from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class BearishInvertedHammerStick(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 1, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        is_bearish_inverted_hammer = open > close;
        is_bearish_inverted_hammer = is_bearish_inverted_hammer and self.approximate_equal(close, low);
        is_bearish_inverted_hammer = is_bearish_inverted_hammer and (open - close) <= 2 * (high - open);

        return is_bearish_inverted_hammer;
