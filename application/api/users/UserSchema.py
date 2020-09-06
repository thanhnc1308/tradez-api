from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    facebook = fields.Str()
    telegram = fields.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
