import datetime
import backtrader as bt
import json
from sqlalchemy import desc, asc
from sqlalchemy import and_, or_, not_
from application.api.stock.StockPriceSchema import stock_price_list_schema
from application.api.stock.StockPrice import StockPrice
from application.api.backtest.strategies.MaCrossoverStrategy import MaCrossoverStrategy
from application.api.backtest.strategies.RSIStrategy import RSIStrategy
from application.api.backtest.strategies.TestStrategy import TestStrategy
import pandas as pd
from application.utility.datetime_utils import subtract_days, is_weekday, parse_date, format_date, get_yesterday_weekday, get_the_day_before_yesterday_weekday
import importlib.util

def backtest_strategy(config):
    cerebro = prepare_cerebro(config)
    data = prepare_feed_data(config)
    cerebro.adddata(data)
    strategy_config = prepare_strategy(config)
    strategy = strategy_config.get('strategy')
    params = strategy_config.get('params')
    cerebro.addstrategy(strategy, **params)
    result = run_backtest(cerebro)
    return result

def prepare_cerebro(config):
    cerebro = bt.Cerebro()
    cash = config.get('cash') or 100000
    cerebro.broker.setcash(cash)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    commission = config.get('commission') or 0.001
    cerebro.broker.setcommission(commission=commission)
    return cerebro

def prepare_feed_data(config):
    symbol = config.get('symbol')
    from_date = config.get('from_date') or '2010-01-01'
    to_date = config.get('to_date') or '2099-12-31'
    sql_data = StockPrice.query.order_by(
        asc('stock_date')
    ).filter(
        and_(
            StockPrice.symbol==symbol,
            StockPrice.stock_date>=from_date,
            StockPrice.stock_date<=to_date
        )
    )
    sql_data = stock_price_list_schema.dump(sql_data)
    def map_row_to_candlestick(row):
        return {
            'Date':parse_date(row['stock_date'], '%Y-%m-%d'),
            'Open': row['open_price'],
            'High': row['high_price'],
            'Low': row['low_price'],
            'Close': row['close_price'],
            'Volume': row['volume']
        }
    sql_data = list(map(map_row_to_candlestick, sql_data))
    df = pd.DataFrame(sql_data)
    df.set_index('Date', inplace=True)
    return bt.feeds.PandasData(dataname=df)

def prepare_strategy(config):
    params = {}
    strategy_name = config.get('strategy')
    strategy_config = get_strategy_config(strategy_name)
    fn_params = strategy_config.get('fn_params')
    return {
        "strategy": strategy_config.get('strategy'),
        "params": fn_params(config)
    }

def get_strategy_config(strategy_name):
    file_path = f'application.api.backtest.strategies.{strategy_name}'
    module = importlib.import_module(file_path)
    strategy = getattr(module, strategy_name)
    fn_params = getattr(module, f'get_{strategy_name}_params')
    return {
        "strategy": strategy,
        "fn_params": fn_params
    }

def run_backtest(cerebro):
    result = []
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    return result
