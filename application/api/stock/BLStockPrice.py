from application.core.constants import DEFAULT_SCHEMA
from application.api.stock.StockPrice import StockPrice
from application.api.stock.StockPriceSchema import stock_price_schema, stock_price_list_schema, stock_price_paging_schema
from sqlalchemy import desc, asc
from application.business.indicators import rsi, ema, sma, adx_dmi, atr, bollinger_band, cci, macd, mfi, parabolic_sar
import pandas as pd

def get_indicators(indicator_str):
    if indicator_str == 'all':
        return []
    else:
        return indicator_str.split('-')

def get_symbols(symbols_str):
    if symbols_str == 'all':
        return []
    else:
        return symbols_str.split('-')

def calculate_indicators_by_list_symbol(list_indicators, list_symbols):
    for symbol in list_symbols:
        print('===================================symbol: ', symbol)
        calculate_indicator_by_symbol(list_indicators, symbol)

def calculate_indicator_by_symbol(indicators, symbol):
    data = StockPrice.query.filter_by(symbol=symbol).order_by(asc('stock_date'))
    df = get_df_stock_price_data(data)
    for indicator in indicators:
        df[indicator] = calculate_by_indicator(indicator, df)
        # print('===================================', df.head())
        print('===================================', df.tail())
    # for row in data:
    #     data_updated = {}
    #     for indicator in indicators:
    #         data_updated[indicator] = calculate_by_indicator(indicator, row)
    #     row.update(**data_updated)
    #     break

def calculate_by_indicator(indicator, df):
    if indicator == 'rsi14':
        df_rsi = rsi.calculate(df=df)
        return df_rsi['RSI']
    elif indicator == 'rsi7':
        df_rsi = rsi.calculate(df=df, length=7)
        return df_rsi['RSI']
    elif indicator == 'ema200':
        df_ema = ema.calculate(df=df)
        return df_ema['ema']
    elif indicator == 'ema100':
        df_ema = ema.calculate(df=df, length=100)
        return df_ema['ema']
    elif indicator == 'ema89':
        df_ema = ema.calculate(df=df, length=89)
        return df_ema['ema']
    elif indicator == 'ema50':
        df_ema = ema.calculate(df=df, length=50)
        return df_ema['ema']
    elif indicator == 'ema34':
        df_ema = ema.calculate(df=df, length=34)
        return df_ema['ema']
    elif indicator == 'ema20':
        df_ema = ema.calculate(df=df, length=20)
        return df_ema['ema']

def calculate_indicator_by_symbol_and_date(indicator, symbol, symbol_date):
    pass

def get_df_stock_price_data(data):
    df = pd.DataFrame(columns=['symbol','stock_date','close'])
    data_json = stock_price_list_schema.dump(data)
    df['symbol'] = list(map(lambda x : x.get('symbol'), data_json))
    df['stock_date'] = list(map(lambda x : x.get('stock_date'), data_json))
    df['close'] = list(map(lambda x : x.get('close_price'), data_json))
    return df
