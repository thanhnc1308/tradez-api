from http import HTTPStatus
from flask import Blueprint, jsonify
from application.api.base.ServiceResponse import ServiceResponse
from flask import request
from application.api.stock.Stock import Stock
from application.api.stock.BLStockScreener import screen_stock
from application.api.stock.StockSchema import stock_schema, stock_list_schema
from application.helpers import verify_token
from application.api.stock import crawler

stock_screener_api = Blueprint('stock_screener_api', __name__, url_prefix='/api/stock_screener')

"""[summary]
Params: string base64 of object
{
    "filters":[{}],
    "sort":[{}],
    "range":[0,150],
    "symbol":,
}
Filters
{
    "type": "RSI", # MACD
    "operation": "less", # equal/greater/in_range(between) [10,12]/crosses_below/eless/not_in_range
    "value": "14"
}
{
    "type": "Candle.LongShadow.Upper",
    "operation": "equal",
    "value": "1"
}
{
    "filter": [{
            "left": "market_cap_basic",
            "operation": "nempty"
        }, {
            "left": "type",
            "operation": "in_range",
            "right": ["stock", "dr", "fund"]
        }, {
            "left": "subtype",
            "operation": "in_range",
            "right": ["common", "", "etf", "unit", "mutual", "money", "reit", "trust"]
        }, {
            "left": "exchange",
            "operation": "in_range",
            "right": ["AMEX", "NASDAQ", "NYSE"]
        }, {
            "left": "ADX",
            "operation": "not_in_range",
            "right": [12, 1e 100]
        }, {
            "left": "High.1M",
            "operation": "eless",
            "right": "high"
        }, {
            "left": "SMA10",
            "operation": "less",
            "right": "SMA20"
        }, {
            "left": "MACD.signal",
            "operation": "less",
            "right": "MACD.macd"
        }, {
            "left": "Stoch.RSI.D",
            "operation": "less",
            "right": "Stoch.RSI.K"
        }
    ],
    "options": {
        "lang": "en"
    },
    "symbols": {
        "query": {
            "types": []
        },
        "tickers": []
    },
    "columns": ["logoid", "name", "Recommend.Other", "ADX", "AO", "ATR", "CCI20", "MACD.macd", "MACD.signal", "Mom", "RSI", "Stoch.K", "Stoch.D", "description", "name", "type", "subtype", "update_mode", "ADX", "ADX DI", "ADX-DI", "ADX DI[1]", "ADX-DI[1]", "AO", "AO[1]", "AO[2]", "CCI20", "CCI20[1]", "MACD.macd", "MACD.signal", "Mom", "Mom[1]", "RSI", "RSI[1]", "Stoch.K", "Stoch.D", "Stoch.K[1]", "Stoch.D[1]"],
    "sort": {
        "sortBy": "market_cap_basic",
        "sortOrder": "desc"
    },
    "range": [0, 150]
}
:
Returns:
    list: list of stock satisfied condition
"""
@stock_screener_api.route('', methods=['POST'])
def stock_screener():
    res = ServiceResponse()
    try:
        params = request.json.copy()
        data = screen_stock(params)
        res.on_success(data=data)
    except Exception as e:
        res.on_exception(e)
    return res.build()
