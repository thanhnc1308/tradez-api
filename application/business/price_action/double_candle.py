from business.price_action import calculator
from business.price_action import single_candle


def is_shooting_star_bearish(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Open'] < price_1['Close']) & (price_0['Open'] > price_1['Close']) & ((price_0['High'] - max(price_0['Open'], price_0['Close'])) >= abs(price_0['Open'] - price_0['Close']) * 3) & (
                (min(price_0['Close'], price_0['Open']) - price_0['Low']) <= abs(price_0['Open'] - price_0['Close'])) & single_candle.is_inverted_hammer(price_0)


def is_shooting_star_bullish(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Open'] > price_1['Close']) & (price_0['Open'] < price_1['Close']) & ((price_0['High'] - max(price_0['Open'], price_0['Close'])) >= abs(price_0['Open'] - price_0['Close']) * 3) & (
                (min(price_0['Close'], price_0['Open']) - price_0['Low']) <= abs(price_0['Open'] - price_0['Close'])) & single_candle.is_inverted_hammer(price_0)


def is_bearish_high_harami(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Close'] > price_1['Open']) & (price_0['Open'] > price_0['Close']) & (price_0['Open'] <= price_1['Close']) & (price_1['Open'] <= price_0['Close']) & ((price_0['Open'] - price_0['Close']) < (price_1['Close'] - price_1['Open']))


def is_bullish_high_harami(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Open'] > price_1['Close']) & (price_0['Close'] > price_0['Open']) & (price_0['Close'] <= price_1['Open']) & (price_1['Close'] <= price_0['Open']) & ((price_0['Close'] - price_0['Open']) < (price_1['Open'] - price_1['Close']))


def is_bearish_high_engulfing(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return ((price_1['Close'] > price_1['Open']) & (price_0['Open'] > price_0['Close'])) & ((price_0['Open'] >= price_1['Close']) & (price_1['Open'] >= price_0['Close'])) & ((price_0['Open'] - price_0['Close']) > (price_1['Close'] - price_1['Open']))


def is_bullish_high_engulfing(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Open'] > price_1['Close']) & (price_0['Close'] > price_0['Open']) & (price_0['Close'] >= price_1['Open']) & (price_1['Close'] >= price_0['Open']) & ((price_0['Close'] - price_0['Open']) > (price_1['Open'] - price_1['Close']))


def is_piercing_line_bullish(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Close'] < price_1['Open']) & (price_0['Close'] > price_0['Open']) & (price_0['Open'] < price_1['Low']) & (price_0['Close'] > price_1['Close']) & (price_0['Close'] > ((price_1['Open'] + price_1['Close']) / 2)) & (
                price_0['Close'] < price_1['Open'])


def is_hanging_man_bullish(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Close'] < price_1['Open']) & (price_0['Open'] < price_1['Low']) & (price_0['Close'] > ((price_1['Open'] + price_1['Close']) / 2)) & (price_0['Close'] < price_1['Open']) & single_candle.is_hammer(price_0)


def is_hanging_man_bearish(price_0, price_1):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    return (price_1['Close'] > price_1['Open']) & (price_0['Close'] > ((price_1['Open'] + price_1['Close']) / 2)) & (price_0['Close'] < price_1['Open']) & single_candle.is_hammer(price_0)


