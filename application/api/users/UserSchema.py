from marshmallow import fields, post_load
from application.api.base.BaseSchema import BaseSchema, BaseListSchema


class UserSchema(BaseSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    facebook = fields.Str()
    telegram = fields.Str()

    @post_load()
    def user_details_strip(self, data):
        data['email'] = data['email'].lower().strip()

    # @validates('username')
    # def validate_username(self, username, **kwargs):
    #     if bool(Contact.query.filter_by(username=username).first()):
    #         raise ValidationError(
    #             '"{username}" username already exists, '
    #             'please use a different username.'.format(username=username)
    #         )


class UserListSchema(BaseListSchema):
    items = fields.List(fields.Nested(UserSchema()))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
users_paging_schema = UserListSchema()
