from flask import Blueprint, jsonify
from application.api.base.ServiceResponse import ServiceResponse
from flask import request
from application.api.backtest.BLBacktest import backtest_strategy

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
        result = backtest_strategy(params)
        res.on_success(data=result)
    except Exception as e:
        res.on_exception(e)
    return res.build()
