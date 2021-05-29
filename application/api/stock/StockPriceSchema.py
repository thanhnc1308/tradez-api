from marshmallow import Schema, fields, post_load, validates, ValidationError
from application.api.stock.StockPrice import StockPrice
from application.api.base.BaseSchema import BaseSchema, BaseListSchema

class StockPriceSchema(BaseSchema):
    symbol = fields.String(required=True)
    stock_date = fields.Date()
    currency_unit = fields.String()
    open_price = fields.Number()
    high_price = fields.Number()
    low_price = fields.Number()
    close_price = fields.Number()
    volume = fields.Number()
    ema200 = fields.Number()
    atr14 = fields.Number()


class StockPriceListSchema(BaseListSchema):
    items = fields.List(fields.Nested(StockPriceSchema()))

stock_price_schema = StockPriceSchema()
stock_price_list_schema = StockPriceSchema(many=True)
stock_price_paging_schema = StockPriceListSchema()
