from marshmallow import fields, post_load, validates, ValidationError
from application.api.base.BaseSchema import BaseSchema, BaseListSchema
from application.api.journal.Journal import Journal


class JournalSchema(BaseSchema):
    user_id = fields.UUID()
    journal_date = fields.Date(required=True)
    symbol = fields.Str(required=True)
    transaction_type = fields.Str(required=True)
    entry = fields.Number()
    exit = fields.Number()
    pnl = fields.Number()
    screenshot = fields.Str()
    comment = fields.Str()


class JournalListSchema(BaseListSchema):
    items = fields.List(fields.Nested(JournalSchema()))


journal_schema = JournalSchema()
journals_schema = JournalSchema(many=True)
journals_paging_schema = JournalListSchema()
