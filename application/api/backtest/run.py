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

if CONFIG['mode'] == 'optimization':
    # Parameters Optimization
    for strat in CONFIG['strategies']:
        cerebro.optstrategy(strat, period=range(14,21))
elif CONFIG['mode'] == 'backtest':
    for strat in CONFIG['strategies']:
        cerebro.addstrategy(strat)
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
