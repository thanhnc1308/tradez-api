from marshmallow import fields, post_load, validates, ValidationError
from application.api.base.BaseSchema import BaseSchema, BaseListSchema
from application.api.journal.Journal import Journal


class JournalSchema(BaseSchema):
    user_id = fields.UUID()
    transaction_date = fields.DateTime(required=True)
    symbol = fields.Str(required=True)
    transaction_type = fields.Str(required=True)
    status = fields.Str(allow_none=True)
    quantity = fields.Number(allow_none=True)
    entry = fields.Number(allow_none=True)
    exit = fields.Number(allow_none=True)
    total_value = fields.Number(allow_none=True)
    pnl = fields.Number(allow_none=True)
    screenshot = fields.Str(required=False, allow_none=True)
    comments = fields.Str(allow_none=True)


class JournalListSchema(BaseListSchema):
    items = fields.List(fields.Nested(JournalSchema()))


journal_schema = JournalSchema()
journals_schema = JournalSchema(many=True)
journals_paging_schema = JournalListSchema()
