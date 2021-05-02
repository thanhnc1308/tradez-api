# python3 application/api/backtest/run.py
import os
import sys
sys.path.append('/home/thanhnc/GR/trading-system')
import backtrader as bt
import datetime

from application.api.backtest.utils import run_strategy, add_analyzers
from application.api.backtest.settings import CONFIG

cerebro = bt.Cerebro()

# Data input
###################################DATA YAHOO##################################
# data = bt.feeds.YahooFinanceData(dataname=CONFIG['asset'],
#                                  fromdate=CONFIG['init_date'],
#                                  todate=CONFIG['end_date'])
# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
# dayfromdate = dt.datetime(2019, 1, 1)
#     # todate = dt.datetime(2020, 1, 1)
#     todate = dt.datetime(2022, 12, 31)
# data0 = bt.feeds.MySQLData(fromdate=minutefromdate, todate=todate, server='localhost', database='Stock', username='trader', password='trader', stockID='TX00', KLine='5', Session=0, timeframe=bt.TimeFrame.Minutes)
#     data1 = bt.feeds.MySQLData(fromdate=dayfromdate, todate=todate, server='localhost', database='Stock', username='trader', password='trader', stockID='TX00', KLine='0', Session=0, timeframe=bt.TimeFrame.Days,
#                                sessionend=dt.time(00, 00))
# eurusd_prices = pd.read_csv('mid_data_4000_H1.csv', parse_dates=True, index_col='Time')

#     feed = bt.feeds.PandasData(dataname=eurusd_prices, timeframe=bt.TimeFrame.Minutes, compression=60)
###################################END DATA YAHOO##################################


###################################DATA LOCAL##################################
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, 'BTC-USD.csv')

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    # Do not pass values before this date
    fromdate=datetime.datetime(2016, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2021, 12, 31),
    reverse=False)
###################################END DATA LOCAL##################################

cerebro.adddata(data)

params = {
    'period': 12,
}

if CONFIG['mode'] == 'optimization':
    # Parameters Optimization
    for strat in CONFIG['strategies']:
        cerebro.optstrategy(strat, period=range(14,21))
elif CONFIG['mode'] == 'backtest':
    for strat in CONFIG['strategies']:
        cerebro.addstrategy(strat, **params)
else:
    raise ValueError('CONFIG["mode"] value should be "backtest", "optimization" or "walk_forward".')

# Analyzer
cerebro = add_analyzers(cerebro)

# Set our desired cash start
cerebro.broker.setcash(100000)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=5)

# Set the commission
cerebro.broker.setcommission(commission=0.002)

# Run Strategy
strats = run_strategy(cerebro)
