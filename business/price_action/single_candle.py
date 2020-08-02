from business.price_action import calculator
from core.constant import CANDLESTICK_PATTERN


def is_bullish_candle(price):
    price = calculator.normalize_price(price)
    return price['Close'] > price['Open']


def is_bearish_candle(price):
    price = calculator.normalize_price(price)
    return price['Close'] < price['Open']


def is_bullish_marubozu(price):
    price = calculator.normalize_price(price)
    return price['Close'] < price['Open']


def is_bearish_marubozu(price):
    price = calculator.normalize_price(price)
    return price['Close'] < price['Open']


def is_doji(price):
    doji_size = 0.1
    return abs((price['Open'] - price['Close']) <= (price['High'] - price['Low']) * doji_size)


def is_hammer(price):
    price = calculator.normalize_price(price)
    return (((price['High'] - price['Low']) > 3 * (price['Open'] - price['Close'])) & ((price['Close'] - price['Low']) / (.001 + price['High'] - price['Low']) > 0.6) & (
                (price['Open'] - price['Low']) / (.001 + price['High'] - price['Low']) > 0.6))


def is_inverted_hammer(price):
    price = calculator.normalize_price(price)
    return (((price['High'] - price['Low']) > 3 * (price['Open'] - price['Close'])) & ((price['High'] - price['Close']) / (.001 + price['High'] - price['Low']) > 0.6) & (
                (price['High'] - price['Open']) / (.001 + price['High'] - price['Low']) > 0.6))


