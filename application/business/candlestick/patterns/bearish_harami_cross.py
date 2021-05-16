from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class BearishHaramiCross(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 2, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]
        prev_candle = self.data.iloc[idx + 1 * self.multi_coeff]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        prev_close = prev_candle[self.close_column]
        prev_open = prev_candle[self.open_column]
        prev_high = prev_candle[self.high_column]
        prev_low = prev_candle[self.low_column]

        is_bearish_harami_cross_pattern = ((prev_open < open) and (prev_close > open) and (prev_close > close)and (prev_open  < low) and (prev_high  > high))
        is_second_day_doji  = self.approximate_equal(open, close)

        return (is_bearish_harami_cross_pattern and is_second_day_doji)