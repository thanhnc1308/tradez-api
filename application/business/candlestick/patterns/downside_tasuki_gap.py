from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class DownsideTasukiGap(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 3, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]
        prev_candle = self.data.iloc[idx + 1 * self.multi_coeff]
        b_prev_candle = self.data.iloc[idx + 2 * self.multi_coeff]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        prev_close = prev_candle[self.close_column]
        prev_open = prev_candle[self.open_column]
        prev_high = prev_candle[self.high_column]
        prev_low = prev_candle[self.low_column]

        b_prev_close = b_prev_candle[self.close_column]
        b_prev_open = b_prev_candle[self.open_column]
        b_prev_high = b_prev_candle[self.high_column]
        b_prev_low = b_prev_candle[self.low_column]

        is_first_bearish       = b_prev_close < b_prev_open
        is_second_bearish      = prev_close < prev_open
        is_third_bullish       = close > open
        is_first_gap_exists     = prev_high < b_prev_low
        is_downside_tasuki_gap  = ((prev_open > open) and (prev_close < open) and (close > prev_open) and (close < b_prev_close))

        return (is_first_bearish and is_second_bearish and is_third_bullish and is_first_gap_exists and is_downside_tasuki_gap)
