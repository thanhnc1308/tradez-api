from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.StockPrice import StockPrice
from application.api.stock.StockPriceSchema import stock_price_schema, stock_price_list_schema
from application.helpers import verify_token
from application.helpers import get_error_response
from application.api.base.ServiceResponse import ServiceResponse
# import numpy as np
# import pandas as pd
from application.utility.datetime_utils import subtract_days
from datetime import date, timedelta

stock_price_api = Blueprint('stock_price_api', __name__, url_prefix='/api/stock_price')

@stock_price_api.route('/historical_price', methods=['GET'])
# @verify_token
def get_historical_price():
    res = ServiceResponse()
    try:
        data = []
        print('request.args', request.args)
        return res.on_success(data=data)
    except Exception as e:
        return get_error_response(e)


@stock_price_api.route('/market_info', methods=['GET'])
# @verify_token
def get_market_info():
    res = ServiceResponse()
    try:
        data = []
        # today = date.today()
        today = date.today()
        today_str = today.strftime('%m/%d/%Y')
        yesterday = subtract_days(today, 1).strftime('%m/%d/%Y')
        the_day_before_yesterday = subtract_days(today, 18).strftime('%m/%d/%Y')
        data.append(today_str)
        data.append(yesterday)
        data.append(the_day_before_yesterday)
        test = StockPrice.find_by(stock_date=the_day_before_yesterday)
        return res.on_success(data=stock_price_list_schema.dumps(test))
    except Exception as e:
        return get_error_response(e)
