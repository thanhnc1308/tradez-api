from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.StockPrice import StockPrice
from application.api.stock.StockSchema import stock_schema, stock_list_schema, stock_paging_schema
from application.helpers import verify_token
from application.api.stock import crawler
from application.helpers import verify_token
from application.api.stock.Stock import Stock
from application.api.base.BaseController import BaseController, BaseListController
from flask_restful import Api

stock_api = Blueprint('stock_api', __name__, url_prefix='/api/stock')
api = Api(stock_api)


class StockController(BaseController):
    model = Stock()
    schema = stock_schema


api.add_resource(StockController, '/<string:id>', endpoint='journal')


class StockListController(BaseListController):
    model = Stock()
    schema = stock_schema
    list_schema = stock_list_schema
    paging_schema = stock_paging_schema


api.add_resource(StockListController, '', endpoint='journals')



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
