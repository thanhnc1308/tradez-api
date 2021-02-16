from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.StockPrice import StockPrice
from application.api.stock.StockPriceSchema import stock_price_schema, stock_price_list_schema, stock_price_paging_schema
from application.helpers import verify_token
from application.helpers import get_error_response
from application.api.base.ServiceResponse import ServiceResponse
# import numpy as np
# import pandas as pd
from application.utility.datetime_utils import subtract_days
from datetime import date, timedelta
from sqlalchemy import desc
from sqlalchemy import and_, or_, not_


stock_price_api = Blueprint('stock_price_api', __name__, url_prefix='/api/stock_price')

@stock_price_api.route('/historical_price/all', methods=['GET'])
# @verify_token
def get_historical_price_all():
    res = ServiceResponse()
    try:
        data = []
        symbol = request.args.get('symbol', "", type=str)
        from_date = request.args.get('from_date', "01/01/2010", type=date)
        to_date = request.args.get('to_date', "01/01/2110", type=date)
        data = StockPrice.query.order_by(desc('updated_at')).filter(
            and_(
                StockPrice.symbol==symbol,
                StockPrice.stock_date>=from_date,
                StockPrice.stock_date<=to_date
            )
        )
        return res.on_success(data=stock_price_list_schema.dump(data))
    except Exception as e:
        return get_error_response(e)


@stock_price_api.route('/historical_price', methods=['GET'])
# @verify_token
def get_historical_price():
    res = ServiceResponse()
    try:
        max_per_page = 100
        data = []
        symbol = request.args.get('symbol', "", type=str)
        from_date = request.args.get('from_date', "01/01/2010", type=date)
        to_date = request.args.get('to_date', "01/01/2110", type=date)
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)
        data = StockPrice.query.order_by(desc('updated_at')).filter(
            and_(
                StockPrice.symbol==symbol,
                StockPrice.stock_date>=from_date,
                StockPrice.stock_date<=to_date
            )
        ).paginate(page, per_page)
        meta = {
            'page': page,
            'per_page': per_page,
            'total': data.total,
            'pages': data.pages,
        }
        result = {
            'items': data.items,
            'meta': meta
        }
        return res.on_success(data=stock_price_paging_schema.dump(result))
    except Exception as e:
        return get_error_response(e)


@stock_price_api.route('/market_info', methods=['GET'])
# @verify_token
def get_market_info():
    res = ServiceResponse()
    try:
        max_per_page = 100
        data = []
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)
        today = date.today()
        today_str = today.strftime('%m/%d/%Y')
        yesterday = subtract_days(today, 1).strftime('%m/%d/%Y')
        the_day_before_yesterday = subtract_days(today, 18).strftime('%m/%d/%Y')

        # TODO: filter stock_date = today and yesterday
        data = StockPrice.query.filter_by(stock_date=the_day_before_yesterday).paginate(page, per_page)

        # TODO: calculate voletile

        meta = {
            'page': page,
            'per_page': per_page,
            'total': data.total,
            'pages': data.pages,
        }
        result = {
            'items': data.items,
            'meta': meta
        }
        return res.on_success(data=stock_price_paging_schema.dump(result))
    except Exception as e:
        return get_error_response(e)
