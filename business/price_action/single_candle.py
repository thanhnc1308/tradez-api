from business.price_action import calculator
from core.constant import CANDLESTICK_PATTERN


def is_bearish_candlestick(candle):
    return float(candle['Close']) < float(candle['Open'])


def is_bullish_candlestick(candle):
    return float(candle['Close']) > float(candle['Open'])


def is_doji(price):
    if calculator.open_close_diff_ratio(price) < CANDLESTICK_PATTERN.DOJI_OPEN_CLOSE_DIFF_RATIO \
            and \
            (calculator.candle_length_and_body_diff_ratio(price) >= CANDLESTICK_PATTERN.constant.DOJI_CANDLE_LENGTH_AND_BODY_RATIO):
        return True
    else:
        return False


def is_pin_bar_up(price):
    if calculator.open_close_diff_ratio(price) < CANDLESTICK_PATTERN.PIN_BAR_BODY_RATIO \
            and \
            calculator.candle_length_and_body_diff_ratio(price) >= CANDLESTICK_PATTERN.PIN_BAR_CANDLE_LENGTH_AND_BODY_RATIO:
        return True
    else:
        return False


def calculate_candle_score(lst_0, lst_1, lst_2):
    open_0, high_0, low_0, close_0 = lst_0[0], lst_0[1], lst_0[2], lst_0[3]
    open_1, high_1, low_1, close_1 = lst_1[0], lst_1[1], lst_1[2], lst_1[3]
    open_2, high_2, low_2, close_2 = lst_2[0], lst_2[1], lst_2[2], lst_2[3]

    doji_size = 0.1

    doji = (abs(open_0 - close_0) <= (high_0 - low_0) * doji_size)

    hammer = (((high_0 - low_0) > 3 * (open_0 - close_0)) & ((close_0 - low_0) / (.001 + high_0 - low_0) > 0.6) & (
                (open_0 - low_0) / (.001 + high_0 - low_0) > 0.6))

    inverted_hammer = (((high_0 - low_0) > 3 * (open_0 - close_0)) & ((high_0 - close_0) / (.001 + high_0 - low_0) > 0.6) & (
                (high_0 - open_0) / (.001 + high_0 - low_0) > 0.6))

    bullishigh_reversal = (open_2 > close_2) & (open_1 > close_1) & doji

    bearishigh_reversal = (open_2 < close_2) & (open_1 < close_1) & doji

    evening_star = (close_2 > open_2) & (min(open_1, close_1) > close_2) & (open_0 < min(open_1, close_1)) & (close_0 < open_0)

    morning_star = (close_2 < open_2) & (min(open_1, close_1) < close_2) & (open_0 > min(open_1, close_1)) & (close_0 > open_0)

    shooting_star_bearish = (open_1 < close_1) & (open_0 > close_1) & ((high_0 - max(open_0, close_0)) >= abs(open_0 - close_0) * 3) & (
                (min(close_0, open_0) - low_0) <= abs(open_0 - close_0)) & inverted_hammer

    shooting_star_bullish = (open_1 > close_1) & (open_0 < close_1) & ((high_0 - max(open_0, close_0)) >= abs(open_0 - close_0) * 3) & (
                (min(close_0, open_0) - low_0) <= abs(open_0 - close_0)) & inverted_hammer

    bearishigh_harami = (close_1 > open_1) & (open_0 > close_0) & (open_0 <= close_1) & (open_1 <= close_0) & ((open_0 - close_0) < (close_1 - open_1))

    bullishigh_harami = (open_1 > close_1) & (close_0 > open_0) & (close_0 <= open_1) & (close_1 <= open_0) & ((close_0 - open_0) < (open_1 - close_1))

    bearishigh_engulfing = ((close_1 > open_1) & (open_0 > close_0)) & ((open_0 >= close_1) & (open_1 >= close_0)) & ((open_0 - close_0) > (close_1 - open_1))

    bullishigh_engulfing = (open_1 > close_1) & (close_0 > open_0) & (close_0 >= open_1) & (close_1 >= open_0) & ((close_0 - open_0) > (open_1 - close_1))

    piercing_line_bullish = (close_1 < open_1) & (close_0 > open_0) & (open_0 < low_1) & (close_0 > close_1) & (close_0 > ((open_1 + close_1) / 2)) & (
                close_0 < open_1)

    hanging_man_bullish = (close_1 < open_1) & (open_0 < low_1) & (close_0 > ((open_1 + close_1) / 2)) & (close_0 < open_1) & hammer

    hanging_man_bearish = (close_1 > open_1) & (close_0 > ((open_1 + close_1) / 2)) & (close_0 < open_1) & hammer

    str_candle = ''
    candle_score = 0

    if doji:
        str_candle = 'doji'
    if evening_star:
        str_candle = str_candle + '/ ' + 'evening_star'
        candle_score = candle_score - 1
    if morning_star:
        str_candle = str_candle + '/ ' + 'morning_star'
        candle_score = candle_score + 1
    if shooting_star_bearish:
        str_candle = str_candle + '/ ' + 'shooting_star_bearish'
        candle_score = candle_score - 1
    if shooting_star_bullish:
        str_candle = str_candle + '/ ' + 'shooting_star_bullish'
        candle_score = candle_score - 1
    if hammer:
        str_candle = str_candle + '/ ' + 'hammer'
    if inverted_hammer:
        str_candle = str_candle + '/ ' + 'inverted_hammer'
    if bearishigh_harami:
        str_candle = str_candle + '/ ' + 'bearishigh_harami'
        candle_score = candle_score - 1
    if bullishigh_harami:
        str_candle = str_candle + '/ ' + 'bullishigh_harami'
        candle_score = candle_score + 1
    if bearishigh_engulfing:
        str_candle = str_candle + '/ ' + 'bearishigh_engulfing'
        candle_score = candle_score - 1
    if bullishigh_reversal:
        str_candle = str_candle + '/ ' + 'bullishigh_engulfing'
        candle_score = candle_score + 1
    if bullishigh_reversal:
        str_candle = str_candle + '/ ' + 'bullishigh_reversal'
        candle_score = candle_score + 1
    if bearishigh_reversal:
        str_candle = str_candle + '/ ' + 'bearishigh_reversal'
        candle_score = candle_score - 1
    if piercing_line_bullish:
        str_candle = str_candle + '/ ' + 'piercing_line_bullish'
        candle_score = candle_score + 1
    if hanging_man_bearish:
        str_candle = str_candle + '/ ' + 'hanging_man_bearish'
        candle_score = candle_score - 1
    if hanging_man_bullish:
        str_candle = str_candle + '/ ' + 'hanging_man_bullish'
        candle_score = candle_score + 1

    # return candle_score
    return candle_score, str_candle