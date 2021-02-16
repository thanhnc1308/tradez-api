from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.StockPrice import StockPrice
from application.api.stock.StockSchema import stock_schema, stock_list_schema
from application.helpers import verify_token
from application.api.stock import crawler
from application.helpers import verify_token

stock_api = Blueprint('stock_api', __name__, url_prefix='/api/stock')

@stock_api.route('/historical_price', methods=['GET'])
def get_historical_price(symbol, from_date, to_date):
    print('request.query', request.query)
    return {
        'ok'
    }


@stock_api.route('/market_info', methods=['GET'])
def get_market_info(symbol, from_date, to_date):
    print('request.query', request.query)
    return {
        'ok'
    }

# @stock_api.route('/all', methods=['GET'])
# def get_all_stock_indices():
#     try:
#         data = crawler.get_all_stock_indices()
#         return {
#             'count': len(data),
#             'data': data
#         }
#     except Exception as e:
#         print(e)

@stock_api.route('/crawl_all', methods=['GET'])
def crawl_all():
    try:
        data = crawler.crawl_all_list()
        return {
            'count': len(data),
            'data': data
        }
    except Exception as e:
        print(e)

@stock_api.route('/crawl/<string:stock_index>', methods=['GET'])
def crawl(stock_index):
    try:
        crawler.crawl(stock_index)
        return 'ok'
    except Exception as e:
        print(e)
