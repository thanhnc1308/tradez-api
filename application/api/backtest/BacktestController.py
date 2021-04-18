from flask import Blueprint, jsonify
from application.api.base.ServiceResponse import ServiceResponse
from flask import request
# from application.api.backtest.BLBacktest import TestStrategy
# from application.helpers import verify_token

backtest_api = Blueprint('backtest_api', __name__, url_prefix='/api/backtest')

"""[summary]
Params:
Returns:
    list
"""
@backtest_api.route('', methods=['POST'])
def backtest():
    res = ServiceResponse()
    try:
        params = request.json.copy()
        print('======================================================================\n')
        # print(params)
        print(params.get('symbol'))
        print(params.get('from_date'))
        print(params.get('to_date'))
        print(params.get('strategy'))
        print(params.get('strategy_params'))
        print(params.get('test'))
        print(params.get('strategy_params').get('upper'))
        data = []
        res.on_success(data=data)
    except Exception as e:
        res.on_exception(e)
    return res.build()
