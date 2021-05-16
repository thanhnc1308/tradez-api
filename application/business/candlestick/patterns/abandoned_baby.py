from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder
from application.business.candlestick.patterns.doji import is_doji


class AbandonedBaby(CandlestickFinder):
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

        is_first_bearish = b_prev_close < b_prev_open;
        doji_exists =  is_doji(prev_open, prev_high, prev_low, prev_close)
        gap_exists = ((prev_high < b_prev_low) and (low > prev_high) and (close > open))
        is_third_bullish  = (high < b_prev_open)
        return (is_first_bearish and doji_exists and gap_exists and is_third_bullish)
