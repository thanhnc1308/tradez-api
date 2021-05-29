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
import backtrader.analyzers as btanalyzers

# class PandasData(bt.feeds.PandasData):
#     lines = ('atr14', 'ema200')
#     params = (
#         ('datetime', None),
#         ('open','open'),
#         ('high','high'),
#         ('low','low'),
#         ('close','close'),
#         ('volume','volume'),
#         ('openinterest',None),
#         ('atr14','atr14'),
#         ('ema200','ema200')
#     )


def backtest_strategy(config):
    list_result = []
    list_stock = config.get("symbol")

    for symbol in list_stock:
        result = do_backtest(symbol, config)
        list_result.append(result)
    return list_result

def do_backtest(symbol, config):
    result = {}
    # cerebro
    cerebro = prepare_cerebro(config)
    # data
    df = prepare_feed_data(symbol, config)
    if len(df) > 0:
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)
        # strategy_config
        strategy_config = prepare_strategy(config)
        # analyzer
        cerebro = add_analyzers(cerebro)
        # strategy
        strategy = strategy_config.get('strategy')
        params = strategy_config.get('params')
        cerebro.addstrategy(strategy, **params)
        # run
        strats = run_backtest(cerebro)
        # result
        result = get_trade_result(symbol, strats, cerebro)
    return result


def prepare_cerebro(config):
    cerebro = bt.Cerebro()
    # cash = config.get('cash') or 100000
    # cerebro.broker.setcash(cash)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    # commission = config.get('commission') or 0.001
    # cerebro.broker.setcommission(commission=commission)
    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=5)
    return cerebro

def add_analyzers(cerebro):
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annual_return')
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade_analyzer')

    # cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio')
    # cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharpe_ratio_a') # sharpe ratio anualized
    # cerebro.addanalyzer(btanalyzers.DrawDown, _name='draw_down')
    # cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    # cerebro.addanalyzer(btanalyzers.Transactions, _name='transactions')
    # cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
    # cerebro.addanalyzer(btanalyzers.TimeDrawDown, _name='time_drawdown')
    # cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')
    # cerebro.addanalyzer(btanalyzers.VWR, _name='vwr') # sharpe ratio with log returns
    # cerebro.addanalyzer(btanalyzers.Calmar, _name='calmar')
    # cerebro.addanalyzer(btanalyzers.LogReturnsRolling, _name='log_returns_rolling')
    # cerebro.addanalyzer(btanalyzers.PeriodStats, _name='periods_stats')
    # cerebro.addanalyzer(btanalyzers.TimeReturn, _name='time_return')
    return cerebro

def prepare_feed_data(symbol, config):
    # symbol = config.get('symbol')
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
    print(sql_data[0])
    def map_row_to_candlestick(row):
        return {
            'Date':parse_date(row['stock_date'], '%Y-%m-%d'),
            'Open': row['open_price'],
            'High': row['high_price'],
            'Low': row['low_price'],
            'Close': row['close_price'],
            'ATR14': row['atr14'],
            'EMA200': row['ema200'],
            'Volume': row['volume']
        }
    sql_data = list(map(map_row_to_candlestick, sql_data))
    df = pd.DataFrame(sql_data)
    if len(sql_data) > 0:
        df.set_index('Date', inplace=True)
    return df

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
    # print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    strats = cerebro.run()
    # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    return strats

def get_trade_result(symbol, strats, cerebro):
    _show_analyzers_end(strats[0])
    final_portfolio = round(cerebro.broker.getvalue(), 2)
    if strats[0] is not None:
        result = strats[0].get_trade_result()
        win_rate = strats[0].get_win_rate()
        total_trades = strats[0].get_total_trades()
        # analyzer = strats[0].analyzers.trade_analyzer.get_analysis()
        # total = analyzer.get('total')
        # if total != None:
        #     total_open = analyzer.total.get('open') or 0
        #     total_closed = analyzer.total.get('closed') or 0
        # else:
        #     total_open = 0
        #     total_closed = 0
        # won = analyzer.get('won')
        # if won != None:
        #     total_won = analyzer.won.get('total') or 0
        # else:
        #     total_won = 0
        total_lost = strats[0].loss_quantity
        # loss = analyzer.get('loss')
        # if loss != None:
        #     total_lost = analyzer.lost.get('total') or 0
        # else:
        #     total_lost = 0
        total_won = strats[0].win_quantity
        # pnl = analyzer.get('pnl')
        # if pnl != None and pnl.get('net') != None:
        #     pnl = round(analyzer.pnl.net.total, 2)
        #     percent_pnl = round(pnl / (final_portfolio - pnl) * 100, 2)
        # else:
        #     pnl = 0
        #     percent_pnl = 0
    return {
        'symbol': symbol,
        'result': result,
        'total_trades': total_trades,
        # 'total_open': total_open,
        # 'total_closed': total_closed,
        'total_won': total_won,
        'total_lost': total_lost,
        'win_rate': win_rate,
        # 'analyzer': analyzer,
        # 'pnl': pnl,
        # 'percent_pnl': percent_pnl,
        # 'final_portfolio': final_portfolio
    }

def _show_analyzers_end(strats):
    print('Annual Return: ' + str(strats.analyzers.annual_return.get_analysis()))
    # print('TradeAnalyzer: ' + str(strats.analyzers.trade_analyzer.get_analysis()))
    # _printTradeAnalysis(strats.analyzers.trade_analyzer.get_analysis())

    # print('Returns: ' + str(strats.analyzers.returns.get_analysis()))
    # print('Transactions: ' + str(strats.analyzers.transactions.get_analysis()))
    # print('Sharpe Ratio: ' + str(strats.analyzers.sharpe_ratio.get_analysis()))
    # print('Sharpe Ratio Annualized: ' + str(strats.analyzers.sharpe_ratio_a.get_analysis())) # sharpe ratio anualized
    # print('Sharpe Ratio Log Returns: ' + str(strats.analyzers.vwr.get_analysis())) # sharpe ratio with log returns
    # print('Draw Down: ' + str(strats.analyzers.draw_down.get_analysis()))
    # print('SQN: ' + str(strats.analyzers.sqn.get_analysis()))
    # print('Time Drawdown: ' + str(strats.analyzers.time_drawdown.get_analysis()))
    # print('Time Return: ' + str(strats.analyzers.time_return.get_analysis()))
    # print('Calmar: ' + str(strats.analyzers.calmar.get_analysis()))
    # print('Log Returns Rolling: ' + str(strats.analyzers.log_returns_rolling.get_analysis()))
    # print('Periods Stats: ' + str(strats.analyzers.periods_stats.get_analysis()))
    # print('PyFolio: ' + str(strats.analyzers.pyfolio.get_analysis()))

def _printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    https://backtest-rookies.com/2017/06/11/using-analyzers-backtrader/
    '''
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total

    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    r1 = [total_open, total_closed,total_won,total_lost]

    header_length = len(h1)

    # Print the rows
    print_list = [h1, r1]
    row_format ="{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))