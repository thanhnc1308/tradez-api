from marshmallow import Schema, fields, post_load, validates, ValidationError
# from application.api.stock.StockPrice import StockPrice
from application.api.base.BaseSchema import BaseSchema, BaseListSchema

class MarketInfoSchema(BaseSchema):
    symbol = fields.String(required=True)
    status = fields.String()
    volatile = fields.Number()


class MarketInfoListSchema(BaseListSchema):
    items = fields.List(fields.Nested(MarketInfoSchema()))

market_info_schema = MarketInfoSchema()
market_info_list_schema = MarketInfoSchema(many=True)
market_info_paging_schema = MarketInfoListSchema()
