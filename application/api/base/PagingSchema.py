from marshmallow import Schema, fields


class LinkSchema(Schema):
    prev = fields.String()
    next = fields.String()
    first = fields.String()
    last = fields.String()


class PagingSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()
    pages = fields.Integer()
    links = fields.Nested(LinkSchema())


paging_schema = PagingSchema()
