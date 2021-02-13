from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.Stock import Stock
from application.api.stock.StockSchema import stock_schema, stock_list_schema
from application.helpers import verify_token
from application.api.stock import crawler

stock_api = Blueprint('stock_api', __name__, url_prefix='/api/stock_filter')


@stock_api.route('', methods=['GET'])
def get_all():
    try:
        data = Stock.get_all()
        return {
            'count': len(data),
            'data': data
        }
    except Exception as e:
        print(e)

# https://api.vietstock.vn/finance/stockfilterover
# ?transNo=14&indicator=RSI&toBuy=80&toSell=20&minVol=100000
# &page=1&pageSize=20&orderBy=1&desc=1&catID=0&sectorID=0

# https://api.vietstock.vn/finance/stockfilter
# ?transNo=10&rate=10&minVol=100000&page=1&pageSize=20&orderBy=2&desc=1&catID=0&sectorID=0

# {"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]},{"left":"RSI","operation":"less","right":30},{"left":"RSI7","operation":"less","right":30}],"options":{"lang":"vi"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["logoid","name","close","change","change_abs","Recommend.All","volume","market_cap_basic","price_earnings_ttm","earnings_per_share_basic_ttm","number_of_employees","sector","description","name","type","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,150]}
# {"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]},{"left":"RSI","operation":"less","right":30},{"left":"RSI7","operation":"less","right":30},{"left":"MACD.macd","operation":"less","right":0},{"left":"MoneyFlow","operation":"less","right":50},{"left":"ChaikinMoneyFlow","operation":"less","right":50}],"options":{"lang":"vi"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["logoid","name","close","change","change_abs","Recommend.All","volume","market_cap_basic","price_earnings_ttm","earnings_per_share_basic_ttm","number_of_employees","sector","description","name","type","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,150]}
# {"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]},{"left":"RSI","operation":"less","right":30},{"left":"RSI7","operation":"less","right":30},{"left":"MACD.macd","operation":"less","right":0},{"left":"MoneyFlow","operation":"less","right":50},{"left":"ChaikinMoneyFlow","operation":"less","right":50},{"left":"Candle.LongShadow.Upper","operation":"equal","right":1}],"options":{"lang":"vi"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["logoid","name","close","change","change_abs","Recommend.All","volume","market_cap_basic","price_earnings_ttm","earnings_per_share_basic_ttm","number_of_employees","sector","description","name","type","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,150]}: 
@stock_api.route('/paging_filter', methods=['GET'])
def get_paging_filter(filter):
    try:
        data = Stock.get_all()
        return {
            'count': len(data),
            'data': data
        }
    except Exception as e:
        print(e)


# {"definitionId":"PriceCrossAboveEMA","id":"1612868163782","options":{"exchange":"","sector":"","type":"","target":"","minAvgVolume5d":200000,"count":1000},"parameters":{"period":2}}
