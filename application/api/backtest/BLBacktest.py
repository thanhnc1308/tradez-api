import os
import sys
sys.path.append('/home/thanhnc/GR/trading-system')
import os.path
import datetime
import backtrader as bt
import json
from application.api.stock.StockPriceSchema import stock_price_list_schema
from application.api.stock.StockPrice import StockPrice
from application.api.backtest.strategy.MaCrossoverStrategy import MaCrossoverStrategy
from application.api.backtest.strategy.TestStrategy import TestStrategy
# python3 application/api/backtest/BLBacktest.py


cerebro = bt.Cerebro()
cerebro.addstrategy(MaCrossoverStrategy)

# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, 'datas.txt')

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2000, 12, 31),
    reverse=False)

# Add the Data Feed to Cerebro
cerebro.adddata(data)

cerebro.broker.setcash(100000.0)
# Set the commission - 0.1% ... divide by 100 to remove the %
cerebro.broker.setcommission(commission=0.001)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
