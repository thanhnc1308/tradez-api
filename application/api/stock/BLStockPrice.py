from application.core.constants import DEFAULT_SCHEMA
from application.api.stock.StockPrice import StockPrice
from application.api.stock.Stock import Stock
from application.api.stock.StockSchema import stock_list_schema
from application.api.stock.StockPriceSchema import stock_price_schema, stock_price_list_schema, stock_price_paging_schema
from sqlalchemy import desc, asc
from application.business.indicators.momentum import rsi, awesome_oscillator, stoch_d, stoch_k, williams_r
from application.business.indicators.volatility import average_true_range, bollinger_hband_indicator, bollinger_lband_indicator, keltner_channel_hband_indicator, keltner_channel_lband_indicator
from application.business.indicators.volume import chaikin_money_flow, money_flow_index, on_balance_volume
from application.business.indicators.trend import ema, sma, macd, macd_signal, adx, cci, aroon_down, aroon_up, psar_up_indicator, psar_down_indicator
from application.business.candlestick.candlestick import single_candle, double_candles, triple_candles
import pandas as pd
import math
from application.utility.datetime_utils import subtract_days

list_all_indicators = [
    'rsi14',
    'rsi7',
    'ema200',
    'ema100',
    'ema89',
    'ema50',
    'ema34',
    'ema20',
    'sma200',
    'sma50',
    'sma20',
    # 'rvi10',
    'obv',
    'adx14',
    'atr14',
    'awesome_oscillator',
    'cci20',
    'cmf20',
    'mfi14',
    'macd_level_12_26',
    'macd_signal_12_26',
    'stochastic_k_14_3_3',
    'stochastic_d_14_3_3',
    'williams_percent_range_14',
    'aroon_up_14',
    'aroon_down_14',
    'bollinger20_hband_indicator',
    'bollinger20_lband_indicator',
    'psar_up_indicator',
    'psar_down_indicator',
    'keltner20_channel_hband_indicator',
    'keltner20_channel_lband_indicator',
    'single_candle',
    'double_candles',
    'triple_candles',
]

list_done_symbol = [
    'A32','AAA','AAM','AAS','AAV','ABB','ABC','ABI','ABR'
]

def get_indicators(indicator_str):
    if indicator_str == 'all':
        return list_all_indicators
    else:
        return indicator_str.split('-')

def get_symbols(symbols_str):
    result = []
    if symbols_str == 'all':
        sql = f'select symbol from public.stock s order by symbol;'
        sql_result = Stock.execute(sql)
        list_symbol = stock_list_schema.dump(sql_result)
        for item in list_symbol:
            if item['symbol'] >= 'DC1':
                result.append(item['symbol'])
        print(len(result))
        # print(result)
    elif str(symbols_str).find('limit') > -1 and str(symbols_str).find('offset') > -1:
        args = symbols_str.split('-')
        limit_str = args[0]
        offset_str = args[1]
        limit = limit_str.split('_')[1]
        offset = offset_str.split('_')[1]
        sql = f'select symbol from public.stock s order by symbol limit {limit} offset {offset};'
        sql_result = Stock.execute(sql)
        list_symbol = stock_list_schema.dump(sql_result)
        for item in list_symbol:
            result.append(item['symbol'])
        # print(result)
    else:
        result = symbols_str.split('-')
    return result

def calculate_indicators_by_list_symbol(list_indicators, list_symbols):
    for symbol in list_symbols:
        print('===================================symbol: ', symbol)
        calculate_indicator_by_symbol(list_indicators, symbol)

def calculate_indicator_by_symbol(indicators, symbol):
    data = StockPrice.query.filter_by(symbol=symbol).order_by(asc('stock_date'))
    df = get_df_stock_price_data(data)
    for indicator in indicators:
        print('===================================indicator', indicator)
        df[indicator] = calculate_by_indicator(indicator, df)
    # print('===================================', df.tail())
    def get_value(value):
        if isinstance(indicator_value, str):
            return str(indicator_value)
        elif indicator_value == None:
            return None
        elif math.isnan(indicator_value) or math.isinf(indicator_value):
            return None
        else:
            return round(indicator_value, 2)
    for row in data:
        data_updated = stock_price_schema.dump(row)
        for indicator in indicators:
            indicator_row = df[df['stock_date'] == data_updated['stock_date']]
            indicator_value = indicator_row[indicator].to_list()[0]
            # print('===================================update indicator', indicator)
            # print('indicator_value: ', indicator_value)
            data_updated[indicator] = get_value(indicator_value)
        # if data_updated['single_candle'] != None:
        # if data_updated['double_candles'] != None:
        # if data_updated['triple_candles'] != None:
        # print(data_up dated)
        row.update(**data_updated)
        # break

def calculate_by_indicator(indicator, df):
    if indicator == 'rsi14':
        return rsi(close=df['close'], window=14)
    elif indicator == 'rsi7':
        return rsi(close=df['close'], window=7)
    elif indicator == 'ema200':
        return ema(close=df['close'], window=200)
    elif indicator == 'ema100':
        return ema(close=df['close'], window=100)
    elif indicator == 'ema89':
        return ema(close=df['close'], window=89)
    elif indicator == 'ema50':
        return ema(close=df['close'], window=50)
    elif indicator == 'ema34':
        return ema(close=df['close'], window=34)
    elif indicator == 'ema20':
        return ema(close=df['close'], window=20)
    elif indicator == 'sma200':
        return sma(close=df['close'], window=200)
    elif indicator == 'sma50':
        return sma(close=df['close'], window=50)
    elif indicator == 'sma20':
        return sma(close=df['close'], window=20)
    elif indicator == 'obv':
        return on_balance_volume(close=df['close'], volume=df['volume'])
    elif indicator == 'adx14':
        return adx(high=df['high'], low=df['low'], close=df['close'], window=14)
    elif indicator == 'atr14':
        return average_true_range(high=df['high'], low=df['low'], close=df['close'], window=14)
    elif indicator == 'awesome_oscillator':
        return awesome_oscillator(high=df['high'], low=df['low'])
    elif indicator == 'cci20':
        return cci(high=df['high'], low=df['low'], close=df['close'], window=20)
    elif indicator == 'cmf20':
        return chaikin_money_flow(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=20)
    elif indicator == 'mfi14':
        return money_flow_index(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=14)
    elif indicator == 'macd_level_12_26':
        return macd(close=df['close'], window_slow=26, window_fast=12)
    elif indicator == 'macd_signal_12_26':
        return macd_signal(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
    elif indicator == 'stochastic_k_14_3_3':
        return stoch_k(high=df['high'], low=df['low'], close=df['close'], window=14, smooth_window=3)
    elif indicator == 'stochastic_d_14_3_3':
        return stoch_d(high=df['high'], low=df['low'], close=df['close'], window=14, smooth_window=3)
    elif indicator == 'williams_percent_range_14':
        return williams_r(high=df['high'], low=df['low'], close=df['close'], lbp=14)
    # elif indicator == 'rvi10':
    #     return ema(close=df['close'], window=20)
    elif indicator == 'bollinger20_hband_indicator':
        return bollinger_hband_indicator(close=df['close'], window=20, window_dev=2)
    elif indicator == 'bollinger20_lband_indicator':
        return bollinger_lband_indicator(close=df['close'], window=20, window_dev=2)
    elif indicator == 'psar_up_indicator':
        return psar_up_indicator(high=df['high'], low=df['low'], close=df['close'], step=0.02, max_step=0.2)
    elif indicator == 'psar_down_indicator':
        return psar_down_indicator(high=df['high'], low=df['low'], close=df['close'], step=0.02, max_step=0.2)
    elif indicator == 'aroon_up_14':
        return aroon_up(close=df['close'], window=14)
    elif indicator == 'aroon_down_14':
        return aroon_down(close=df['close'], window=14)
    elif indicator == 'keltner20_channel_hband_indicator':
        return keltner_channel_hband_indicator(high=df['high'], low=df['low'], close=df['close'], window=20, window_atr=10)
    elif indicator == 'keltner20_channel_lband_indicator':
        return keltner_channel_lband_indicator(high=df['high'], low=df['low'], close=df['close'], window=20, window_atr=10)
    elif indicator == 'single_candle':
        return single_candle(df)
    elif indicator == 'double_candles':
        return double_candles(df)
    elif indicator == 'triple_candles':
        return triple_candles(df)

def get_df_stock_price_data(data):
    df = pd.DataFrame(columns=['symbol','stock_date','open','high','low','close','volume'])
    data_json = stock_price_list_schema.dump(data)
    df['symbol'] = list(map(lambda x : x.get('symbol'), data_json))
    df['stock_date'] = list(map(lambda x : x.get('stock_date'), data_json))
    df['open'] = list(map(lambda x : x.get('open_price'), data_json))
    df['high'] = list(map(lambda x : x.get('high_price'), data_json))
    df['low'] = list(map(lambda x : x.get('low_price'), data_json))
    df['close'] = list(map(lambda x : x.get('close_price'), data_json))
    df['volume'] = list(map(lambda x : x.get('volume'), data_json))
    return df

def calculate_indicators_by_list_symbol_in_a_date(list_indicators, list_symbols, date):
    for symbol in list_symbols:
        print('===================================symbol: ', symbol)
        calculate_indicator_by_symbol_and_date(list_indicators, symbol, date)

def calculate_indicator_by_symbol_and_date(indicators, symbol, date):
    from_date = subtract_days(date, 210)
    data = StockPrice.query.filter(StockPrice.symbol==symbol, StockPrice.stock_date >= from_date).order_by(asc('stock_date'))
    df = get_df_stock_price_data(data)
    for indicator in indicators:
        print('===================================indicator', indicator)
        df[indicator] = calculate_by_indicator(indicator, df)
    print('===================================', df.tail())
    count = 0
    for row in data:
        data_updated = stock_price_schema.dump(row)
        for indicator in indicators:
            indicator_row = df[df['stock_date'] == data_updated['stock_date']]
            indicator_value = indicator_row[indicator].to_list()[0]
            print('===================================indicator', indicator)
            data_updated[indicator] = round(indicator_value, 2) if not (math.isnan(indicator_value) or indicator_value == None or math.isinf(indicator_value)) else None
        # count = count + 1
        # if count == 200:
        #     print(data_updated)
        # row.update(**data_updated)
            # break