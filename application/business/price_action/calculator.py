def normalize_price(price):
    price['High'] = float(price['High'])
    price['Low'] = float(price['Low'])
    price['Open'] = float(price['Open'])
    price['Close'] = float(price['Close'])
    return price


def open_price_close_price_diff_ratio(price):
    high_price = float(price['High'])
    low_price = float(price['Low'])
    open_price = float(price['Open'])
    close_price = float(price['Close'])
    return abs(close_price - open_price)/open_price


def candle_length_and_body_diff_ratio(price):
    return candle_length(price)/body_length(price)


def upper_shadow(price):
    high_price = float(price['High'])
    low_price = float(price['Low'])
    open_price = float(price['Open'])
    close_price = float(price['Close'])
    if close_price > open_price: # if bullish
        return high_price - close_price
    else:
        return high_price - open_price


def lower_shadow(price):
    high_price = float(price['High'])
    low_price = float(price['Low'])
    open_price = float(price['Open'])
    close_price = float(price['Close'])
    if close_price > open_price: # if bullish
        return open_price - low_price
    else:
        return close_price - low_price


def body_length(price):
    high_price = float(price['High'])
    low_price = float(price['Low'])
    open_price = float(price['Open'])
    close_price = float(price['Close'])
    return abs(close_price - open_price)


def candle_length(price):
    high_price = float(price['High'])
    low_price = float(price['Low'])
    open_price = float(price['Open'])
    close_price = float(price['Close'])
    return high_price - low_price
