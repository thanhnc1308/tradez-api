from business.price_action import single_candle


def is_bullish_engulfing(current_day, previous_day):
    if single_candle.is_bearish_candlestick(previous_day) \
            and current_day['Close'] > previous_day['Open'] \
            and current_day['Open'] < previous_day['Close']:
        return True
    else:
        return False
