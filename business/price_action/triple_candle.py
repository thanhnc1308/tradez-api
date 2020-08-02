from business.price_action import calculator
from business.price_action import single_candle


def is_bullish_high_reversal(price_0, price_1, price_2):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    price_2 = calculator.normalize_price(price_2)
    return (price_2['Open'] > price_2['Close']) & (price_1['Open'] > price_1['Close']) & single_candle.is_doji(price_0)


def is_bearish_high_reversal(price_0, price_1, price_2):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    price_2 = calculator.normalize_price(price_2)
    return (price_2['Open'] < price_2['Close']) & (price_1['Open'] < price_1['Close']) & single_candle.is_doji(price_0)


def is_evening_star(price_0, price_1, price_2):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    price_2 = calculator.normalize_price(price_2)
    return (price_2['Close'] > price_2['Open']) & (min(price_1['Open'], price_1['Close']) > price_2['Close']) & (price_0['Open'] < min(price_1['Open'], price_1['Close'])) & (price_0['Close'] < price_0['Open'])


def is_morning_star(price_0, price_1, price_2):
    price_0 = calculator.normalize_price(price_0)
    price_1 = calculator.normalize_price(price_1)
    price_2 = calculator.normalize_price(price_2)
    return (price_2['Close'] < price_2['Open']) & (min(price_1['Open'], price_1['Close']) < price_2['Close']) & (price_0['Open'] > min(price_1['Open'], price_1['Close'])) & (price_0['Close'] > price_0['Open'])


