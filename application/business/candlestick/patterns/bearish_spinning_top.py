from application.business.candlestick.patterns.candlestick_finder import CandlestickFinder


class BearishSpinningTop(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 1, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        body_length           = abs(close-open)
        upper_shadow_length    = abs(high-open)
        lower_shadow_length    = abs(high-low)
        is_bearish_spinning_top = body_length < upper_shadow_length and body_length < lower_shadow_length

        return is_bearish_spinning_top
