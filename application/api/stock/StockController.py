from http import HTTPStatus
from flask import Blueprint, jsonify
from flask import request
from application.api.stock.Stock import Stock
from application.api.stock.StockSchema import stock_schema, stock_list_schema

stock_api = Blueprint('stock_api', __name__, url_prefix='/api/stock')


@stock_api.route('', methods=["GET"])
@stock_api.route('<string:id>', methods=["GET"])
def retrieve_stock(id=None):
    if id:
        stock = Stock.query.filter_by(id=id).first_or_404()
        res = stock_schema.dump(stock)
        return res, HTTPStatus.OK

    stock = Stock.query.all()
    res = stock_list_schema.dump(stock)
    return jsonify(res), HTTPStatus.OK


@stock_api.route('', methods=["POST"])
def create_stock():
    data = request.get_json()
    print('data: ', data)
    validated_data, errors = stock_schema.load(data)
    if errors:
        return jsonify('errors'), HTTPStatus.BAD_REQUEST
    return stock_schema.dump(stock_schema.instance), HTTPStatus.CREATED


@stock_api.route('/<string:id>', methods=["PUT", "PATCH"])
def update_stock(id):
    stock = Stock.query.filter_by(id=id).first_or_404()

    data = request.get_json()

    schema = stock_schema
    if request.method == 'PATCH':
        errors = schema.validate(data, partial=True)
    else:
        errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    schema.update_stock(stock, data)
    updated_stock = Stock.query.filter_by(id=stock.id).first()
    return stock_schema.dump(updated_stock), HTTPStatus.ACCEPTED


@stock_api.route('/<string:id>', methods=["DELETE"])
def delete_stock(id):
    stock = Stock.query.filter_by(id=id).first_or_404()
    stock.delete()
    return jsonify(id), HTTPStatus.NO_CONTENT
