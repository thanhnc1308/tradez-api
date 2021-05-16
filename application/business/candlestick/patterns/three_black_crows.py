from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class ThreeBlackCrows(CandlestickFinder):
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

        is_down_trend = b_prev_low > prev_low and prev_low > low;
        is_all_bearish = b_prev_open > b_prev_close and prev_open > prev_close and open > close;

        does_open_within_previous_body  = b_prev_open > prev_open and prev_open > b_prev_close and prev_open > open  and open > prev_close

        return (is_down_trend and is_all_bearish and does_open_within_previous_body)
