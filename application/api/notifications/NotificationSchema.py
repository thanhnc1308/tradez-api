from marshmallow import Schema, fields, post_load, validates, ValidationError
from application.api.base.BaseSchema import BaseSchema, BaseListSchema
from application.api.notifications.Notification import Notification

class NotificationSchema(BaseSchema):
    user_id = fields.UUID()
    condition = fields.Nested(ConditionSchema)
    gmail = fields.Str()
    tg_chat_id = fields.Str()
    send_gmail = fields.Boolean()
    send_telegram = fields.Boolean()

class ConditionSchema(Schema):
    filter_type = fields.String()
    filter_value = fields.String()
    filter_operation = fields.String()

class NotificationListSchema(BaseListSchema):
    items = fields.List(fields.Nested(NotificationSchema()))


notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
notifications_paging_schema = NotificationListSchema()
