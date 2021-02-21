from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.StockPrice import StockPrice
from application.api.stock.StockPriceSchema import stock_price_schema, stock_price_list_schema, stock_price_paging_schema
from application.api.stock.MarketInfoSchema import market_info_paging_schema
from application.helpers import verify_token
from application.api.base.ServiceResponse import ServiceResponse
# import numpy as np
import pandas as pd
from application.utility.datetime_utils import subtract_days, is_weekday, parse_date, format_date, get_yesterday_weekday, get_the_day_before_yesterday_weekday
from datetime import date, timedelta, datetime
from sqlalchemy import desc, asc
from sqlalchemy import and_, or_, not_
from decimal import Decimal


stock_price_api = Blueprint('stock_price_api', __name__, url_prefix='/api/stock_price')

@stock_price_api.route('/historical_price/all', methods=['GET'])
@verify_token
def get_historical_price_all(current_user):
    res = ServiceResponse()
    try:
        data = []
        symbol = request.args.get('symbol', "", type=str)
        from_date = request.args.get('from_date', "01/01/2010", type=str)
        to_date = request.args.get('to_date', "01/01/2110", type=str)
        data = StockPrice.query.order_by(asc('updated_at')).filter(
            and_(
                StockPrice.symbol==symbol,
                StockPrice.stock_date>=from_date,
                StockPrice.stock_date<=to_date
            )
        )
        data = stock_price_list_schema.dump(data)
        def map_row_to_candlestick(row):
            return {
            'x': parse_date(row['stock_date'], '%Y-%m-%d'),
            'y': [row['open_price'],row['high_price'],row['low_price'],row['close_price']]
        }
        data = list(map(map_row_to_candlestick, data))
        res.on_success(data=data)
    except Exception as e:
        res.on_exception(e)
    return res.build()


@stock_price_api.route('/historical_price', methods=['GET'])
@verify_token
def get_historical_price(current_user):
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
        res.on_success(data=stock_price_paging_schema.dump(result))
    except Exception as e:
        res.on_exception(e)
    return res.build()


@stock_price_api.route('/market_info', methods=['GET'])
@verify_token
def get_market_info(current_user):
    res = ServiceResponse()
    try:
        max_per_page = 100
        data = []
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)
        # today_date = date.today()
        today_date = parse_date('12/01/2021')
        if is_weekday(today_date):
            today = format_date(today_date)
            yesterday = format_date(get_yesterday_weekday(today_date))
            the_day_before_yesterday = format_date(get_the_day_before_yesterday_weekday(today_date))
            data = StockPrice.query.order_by(desc('updated_at')).filter(
                or_(
                    StockPrice.stock_date==today,
                    StockPrice.stock_date==yesterday,
                    StockPrice.stock_date==the_day_before_yesterday
                )
            ).paginate(page, per_page)
            # calculate voletile
            df = pd.DataFrame(columns=['symbol','today','yesterday'])
            today_data = StockPrice.query.order_by(desc('updated_at')).filter(StockPrice.stock_date==today).paginate(page, per_page)
            yesterday_data = StockPrice.query.order_by(desc('updated_at')).filter(StockPrice.stock_date==yesterday).paginate(page, per_page)
            the_day_before_yesterday_data = StockPrice.query.order_by(desc('updated_at')).filter(StockPrice.stock_date==the_day_before_yesterday).paginate(page, per_page)
            df['symbol'] = list(map(lambda x : x.symbol, today_data.items))
            df['today'] = list(map(lambda x : x.close_price, today_data.items))
            df['yesterday'] = list(map(lambda x : x.close_price, yesterday_data.items))
            df['volatile'] = df.apply(lambda x : round(((x['today']) - x['yesterday']) / x['today'] * 100, 2), axis=1)
            meta = {
                'page': page,
                'per_page': per_page,
                'total': today_data.total,
                'pages': today_data.pages,
            }
            result = {
                'items': df.to_dict('records'),
                'meta': meta
            }
            res.on_success(data=market_info_paging_schema.dump(result))
        res.on_success(data=[])
    except Exception as e:
        res.on_exception(e)
    return res.build()
