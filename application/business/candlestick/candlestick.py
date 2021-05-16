import re
BASE_PATH = 'application.business.candlestick.patterns.'
import sys
import pandas as pd
import numpy as np

this_module = sys.modules[__name__]

__builders = dict()
__default_ohlc = ['open', 'high', 'low', 'close']

list_single_candle = [
    'doji',
    'gravestone_doji',
    'dragonfly_doji',
    'hammer',
    'inverted_hammer',
    'bullish_marubozu',
    'bearish_marubozu',
    'bearish_hammer_stick',
    'bearish_inverted_hammer_stick',
    'bullish_inverted_hammer_stick',
    'bearish_spinning_top',
    'bullish_spinning_top',
    'bullish_hammer_stick',
]

list_double_candles = [
    'bullish_harami',
    'bearish_harami',
    'dark_cloud_cover',
    'doji_star',
    'bearish_engulfing',
    'bullish_engulfing',
    'piercing_pattern',
    'rain_drop',
    'rain_drop_doji',
    'star',
    'shooting_star',
    'bearish_harami_cross',
    'bullish_harami_cross',
    'inside_bar',
    'outside_bar',
]

list_triple_candles = [
    'hanging_man',
    'morning_star',
    'morning_star_doji',
    'evening_star',
    'evening_star_doji',
    'abandoned_baby',
    'downside_tasuki_gap',
    'three_black_crows',
    'three_white_soldiers',
    'three_outside_down',
    'three_outside_up',
    'three_inside_up',
    'three_inside_down',
]

def single_candle(candles_df):
    candles_df['single_candle'] = None
    def get_candle_name(x):
        result = ''
        current_pattern = x['single_candle']
        if x[snake_case_to_pascal_case(pattern)] == True:
            if current_pattern == None:
                result = pattern
            else:
                result = f"{current_pattern}_{pattern}"
        else:
            result = current_pattern
        return result
    for pattern in list_single_candle:
        fn = getattr(this_module, pattern)
        candles_df = fn(candles_df)
        candles_df['single_candle'] = candles_df.apply(lambda x : get_candle_name(x), axis=1)
    return pd.Series(data=candles_df['single_candle'], name='single_candle')

def double_candles(candles_df):
    candles_df['double_candles'] = None
    def get_candle_name(x):
        result = ''
        current_pattern = x['double_candles']
        if x[snake_case_to_pascal_case(pattern)] == True:
            if current_pattern == None:
                result = pattern
            else:
                result = f"{current_pattern}_{pattern}"
        else:
            result = current_pattern
        return result
    for pattern in list_double_candles:
        fn = getattr(this_module, pattern)
        candles_df = fn(candles_df)
        candles_df['double_candles'] = candles_df.apply(lambda x : get_candle_name(x), axis=1)
    return pd.Series(data=candles_df['double_candles'], name='double_candles')

def triple_candles(candles_df):
    candles_df['triple_candles'] = None
    def get_candle_name(x):
        result = ''
        current_pattern = x['triple_candles']
        if x[snake_case_to_pascal_case(pattern)] == True:
            if current_pattern == None:
                result = pattern
            else:
                result = f"{current_pattern}_{pattern}"
        else:
            result = current_pattern
        return result
    for pattern in list_triple_candles:
        fn = getattr(this_module, pattern)
        candles_df = fn(candles_df)
        candles_df['triple_candles'] = candles_df.apply(lambda x : get_candle_name(x), axis=1)
    return pd.Series(data=candles_df['triple_candles'], name='triple_candles')

def snake_case_to_pascal_case(s):
    return str(''.join(word.title() for word in s.split('_')))

def __get_file_name(class_name):
    res = re.findall('[A-Z][^A-Z]*', class_name)
    return '_'.join([cur.lower() for cur in res])


def __load_module(module_path):
    p = module_path.rfind('.') + 1
    super_module = module_path[p:]
    try:
        # print(module_path)
        module = __import__(module_path, fromlist=[super_module], level=0)
        return module
    except ImportError as e:
        raise e


def __get_class_by_name(class_name):
    file_name = __get_file_name(class_name)
    mod_name = BASE_PATH + file_name

    if mod_name not in __builders:
        module = __load_module(mod_name)
        __builders[mod_name] = module
    else:
        module = __builders[mod_name]
    return getattr(module, class_name)


def __create_object(class_name, target):
    return __get_class_by_name(class_name)(target=target)


#region single candle

def doji(candles_df,
         ohlc=__default_ohlc,
         is_reversed=False,
         target=None):
    doji = __create_object('Doji', target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)

def gravestone_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    gs_doji = __create_object('GravestoneDoji', target)
    return gs_doji.has_pattern(candles_df, ohlc, is_reversed)

def dragonfly_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    doji = __create_object('DragonflyDoji', target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)

def hammer(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('Hammer', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def inverted_hammer(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('InvertedHammer', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bullish_marubozu(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishMarubozu', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_marubozu(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishMarubozu', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_hammer_stick(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishHammerStick', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bullish_hammer_stick(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishHammerStick', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_inverted_hammer_stick(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishInvertedHammerStick', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bullish_inverted_hammer_stick(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishInvertedHammerStick', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_spinning_top(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishSpinningTop', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bullish_spinning_top(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishSpinningTop', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

# def bullish_hanging_man(candles_df,
#                    ohlc=__default_ohlc,
#                    is_reversed=False,
#                    target=None):
#     bullhm = __create_object('BullishHangingMan', target)
#     return bullhm.has_pattern(candles_df, ohlc, is_reversed)

#region double candle

def bearish_harami(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bear_harami = __create_object('BearishHarami', target)
    return bear_harami.has_pattern(candles_df, ohlc, is_reversed)

def bullish_harami(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bull_harami = __create_object('BullishHarami', target)
    return bull_harami.has_pattern(candles_df, ohlc, is_reversed)

def dark_cloud_cover(candles_df,
                     ohlc=__default_ohlc,
                     is_reversed=False,
                     target=None):
    dcc = __create_object('DarkCloudCover', target)
    return dcc.has_pattern(candles_df, ohlc, is_reversed)

def doji_star(candles_df,
              ohlc=__default_ohlc,
              is_reversed=False,
              target=None):
    doji = __create_object('DojiStar', target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)

def bearish_engulfing(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishEngulfing', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bullish_engulfing(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishEngulfing', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def piercing_pattern(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('PiercingPattern', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def rain_drop(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('RainDrop', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def rain_drop_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('RainDropDoji', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('Star', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def shooting_star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ShootingStar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_harami_cross(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishHaramiCross', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bullish_harami_cross(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishHaramiCross', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def inside_bar(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('InsideBar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def outside_bar(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('OutsideBar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

#region triple candle

def hanging_man(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bearhm = __create_object('HangingMan', target)
    return bearhm.has_pattern(candles_df, ohlc, is_reversed)

def morning_star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('MorningStar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def morning_star_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('MorningStarDoji', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def evening_star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('EveningStar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def evening_star_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('EveningStarDoji', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def abandoned_baby(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('AbandonedBaby', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def downside_tasuki_gap(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('DownsideTasukiGap', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_black_crows(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeBlackCrows', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_white_soldiers(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeWhiteSoldiers', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_outside_down(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeOutsideDown', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_outside_up(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeOutsideUp', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_inside_up(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeInsideUp', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_inside_down(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeInsideDown', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)
